import sys
import os
sys.path.append("/app/src")

from embedding_tasks import echo_task

# RQ worker запускается через команду в docker-compose, отдельный запуск не требуется.
# Этот файл нужен для импорта задач. 