import time
import random
from redis import Redis
import os

def llm_task(embedding_result: str, job_id: str) -> None:
    sleep_time = random.uniform(0.1, 2)
    time.sleep(sleep_time)
    final_result = f"{embedding_result} processed by llm (slept {sleep_time:.2f}s)"
    redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
    redis_conn = Redis.from_url(redis_url)
    redis_conn.set(f"result:{job_id}", final_result) 