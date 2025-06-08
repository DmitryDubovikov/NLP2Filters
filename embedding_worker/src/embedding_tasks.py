import random
import time
from redis import Redis
from rq import Queue
import os

def echo_task(text: str, job_id: str) -> None:
    sleep_time = random.uniform(0.1, 2)
    time.sleep(sleep_time)
    result = f"Echo: {text} (slept {sleep_time:.2f}s)"
    redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
    redis_conn = Redis.from_url(redis_url)
    llm_queue = Queue("llm", connection=redis_conn)
    llm_queue.enqueue("llm_tasks.llm_task", result, job_id)
