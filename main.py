import platform
import time

import dotenv
import os
from Process import Process

dotenv.load_dotenv()

API_TOKEN: str = os.getenv('BOT_MANAGER')
ADMIN_ID: int = int(os.getenv('ADMIN_ID'))


def __parse_workers_folder() -> list[str]:
    return list(os.listdir("./Workers/"))


if __name__ == "__main__":
    for string in __parse_workers_folder():
        print(string)
    if platform.system() == "Windows":
        python_executor = r"venv/Scripts/python.exe"
    else:
        python_executor = r"venv/bin/python3.11"
    exec_path = os.path.abspath('')
    print(f"{exec_path = }")
    processes = {"TelegramPastaPosterBot": Process(name="TelegramPastaPosterBot",
                                                   exec_path=exec_path + "/Workers/TelegramPastaBot/",
                                                   python_executor=python_executor),
                 "TelegramWalletBot": Process(name="TelegramWalletBot",
                                              exec_path=exec_path + "/Workers/TGbotWallet/",
                                              python_executor=python_executor)}
    {process.start() for process in processes.values()}
