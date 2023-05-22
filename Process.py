import time
from subprocess import Popen, PIPE, call
import subprocess
import threading
import logging


class Process:
    def __init__(self, name: str = "",
                 exec_path: str = r"",
                 git: str = r"",
                 uid: int = 0):
        self.name = name
        self.exec_path = exec_path
        self.git = git
        self.uid = uid
        self.log_path = str()
        self.error_path = str()
        self.error_notification: bool = True
        self.status: str = "Running"
        self.thr = threading.Thread(target=self.__start_proc).start()

    def on_log(self, string: str = ""):
        print(string, flush=True)

    def on_error(self, string: str = ""):
        print(string, flush=True)

    def __start_proc(self) -> subprocess:
        process = subprocess.Popen(
            self.exec_path,
            stdout=subprocess.PIPE,
            shell=True,
            encoding='cp866',
            errors='replace')
        self.status = "running"
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                self.status = "stopped"
                break
            if output:
                self.on_log(output)
        print(self)

    def __repr__(self):
        return f"{self.name} with {self.uid} uid is {self.status}"


if __name__ == "__main__":
    ping_proc = Process(name="Ping proc",
                        exec_path="ping 10.10.1.1")
