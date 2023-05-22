import os
import asyncio
import subprocess
import threading
import dotenv
import select

dotenv.load_dotenv()

# API_TOKEN: str = os.getenv('BOT_TOKEN')
# ADMIN_ID: int = int(os.getenv('ADMIN_ID'))


# def main() -> list[threading.Thread]:
#     w = threading.Thread(target=subprocess.run, args=["python.exe wait.py"])
#     t = threading.Thread(target=subprocess.run, args=["python.exe print.py"])
#     return [w, t]
#
#
# if __name__ == "__main__":
#     [thr.start() for thr in main()]


import asyncio
import subprocess

process = subprocess.Popen(
    'ping 10.10.0.1',
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    shell=True,
    encoding='cp866',
    errors='replace'
)

while True:
    realtime_output = process.stdout.readline()

    if realtime_output == '' and process.poll() is not None:
        break

    if realtime_output:
        print(realtime_output.strip(), flush=True)

""" В этом примере мы создаем асинхронную функцию `run_command`,
    которая запускает процесс подобно методу `run()` с использованием модуля `subprocess`.
    Затем мы используем `communicate()` для чтения данных со стандартных потоков вывода и ошибок.
    Если в результате работы процесса возникнет ошибка, то значение `code` будет отлично от нуля,
    и мы можем обработать ошибку соответствующим образом.
"""
