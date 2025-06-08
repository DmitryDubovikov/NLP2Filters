from flask import Blueprint, request, jsonify
import redis
from rq import Queue
from rq.job import Job
import os
import uuid

embedding_bp = Blueprint("embedding", __name__)

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis_conn = redis.from_url(redis_url)
embedding_queue = Queue("embedding", connection=redis_conn)

def enqueue_echo_task(text: str) -> str:
    job_id = str(uuid.uuid4())
    embedding_queue.enqueue("embedding_tasks.echo_task", text, job_id, job_id=job_id)
    return job_id

def get_job_result(job_id: str):
    # Проверяем финальный результат в Redis
    result = redis_conn.get(f"result:{job_id}")
    if result:
        return {"result": result.decode()}
    # Проверяем статус embedding job
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        if job.is_failed:
            return {"error": "Job failed"}
        return {"status": job.get_status()}
    except Exception:
        return {"status": "pending"}

@embedding_bp.route("/embedding/echo", methods=["POST"])
def embedding_echo():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400
    job_id = enqueue_echo_task(data["text"])
    return jsonify({"job_id": job_id}), 202

@embedding_bp.route("/embedding/result/<job_id>", methods=["GET"])
def embedding_result(job_id):
    result = get_job_result(job_id)
    return jsonify(result) 