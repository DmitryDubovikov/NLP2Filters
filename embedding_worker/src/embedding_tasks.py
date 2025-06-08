import random
import time

def echo_task(text: str) -> str:
   sleep_time = random.uniform(0.1, 2)
   time.sleep(sleep_time)
   return f"Echo: {text} (slept {sleep_time:.2f}s)"