import os
import platform
import time
from loguru import logger
import subprocess
import threading


class Process:
    LAST = 0
    enc = "cp866" if platform.system() == "Windows" else "utf-8"

    @staticmethod
    def __make_filter(name, level):
        def __filter(record):
            return record["extra"].get("name") == name and level == record["level"].name

        return __filter

    def __init__(self, name: str = ".",
                 exec_path: str = r".",
                 main_py_file: str = r"main.py",
                 python_executor: str = r"/venv/Scripts/python.exe",
                 uid: int = 0):
        self.name = name
        self.exec_path = exec_path
        self.main_py_file = main_py_file
        self.python_executor = python_executor
        self.log_path = f"log/{name}.log"
        self.error_path = f"log/{name}_error.log"
        if not uid:
            self.uid = self.LAST
            self.__class__.LAST += 1
        self.__status: str = "Stopped"
        self.__stop = True
        logger.add(self.log_path, level="INFO", rotation="100 MB",
                   filter=self.__make_filter(self.name, "INFO"))
        logger.add(self.error_path, level="ERROR",
                   filter=self.__make_filter(self.name, "ERROR"))
        self._log = logger.bind(name=f"{name}")

        self.error_notification: bool = True
        self.info_notification: bool = False

    def on_start(self):
        self._log.info(self)

    def on_stop(self):
        self._log.info(self)

    def on_log(self, string: str = ""):
        if string != "\n":
            self._log.info(string.strip("\n"))
        if self.info_notification:
            ...

    # Don't work
    def on_error(self, string: str = ""):
        self._log.error(string.rstrip("\n"))
        if self.error_notification:
            ...

    def start(self):
        self.__stop = False
        threading.Thread(target=self.__logging).start()
        self.__process = self.__start_proc()
        self.__status = "running"
        self.on_start()

    def stop(self):
        if not self.__stop:
            self.__stop = True
            self.__process.kill()
            self.__status = "stopped"
            self.on_stop()
        else:
            self._log.info("Already stopped")

    def status(self):
        return str(self)

    def __start_proc(self):
        ex = f"{self.exec_path + self.python_executor} {self.exec_path + self.main_py_file}"
        print(ex)
        return subprocess.Popen(ex,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                cwd=f"{self.exec_path}",
                                encoding=self.enc,
                                errors='replace')

    def update(self):
        self.stop()
        updater = subprocess.Popen(f"git pull",
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   cwd=f"{self.exec_path}",
                                   shell=True,
                                   encoding=self.enc,
                                   errors='replace')
        while True:
            realtime_output = updater.stdout.readline()

            if realtime_output == '' and updater.poll() is not None:
                break
            if realtime_output:
                self._log.info(realtime_output.strip())
        [self.on_error(error) for error in updater.stderr.readlines() if error]
        while updater.wait():
            time.sleep(0.5)
        return self.log()

    def __logging(self):
        while not self.__stop:
            try:
                output = self.__process.stdout.readline()
                if output == '' and self.__process.poll() is not None:
                    self.__status = "stopped"
                    break
                if output:
                    self.on_log(output)
            except AttributeError:
                ...
        try:
           [self.on_error(error) for error in self.__process.stderr.readlines() if error]
        except AttributeError:
            ...

    def __str__(self):
        return f"{self.name} with {self.uid} uid is {self.__status}"

    def log(self):
        with open(self.log_path, "r") as file:
            return "".join(file.readlines(0)[-6::]) or "EMPTY"

    def error_log(self):
        with open(self.error_path, "r") as file:
            return "".join(file.readlines(0)[-15::]) or "EMPTY"


if __name__ == "__main__":
    n = 200
    ping1 = Process(name="Ping1", exec_path=f"ping 1.1.1.1 -n {n}")
    # ping1.start()

    # ping2 = Process(name="Ping2", exec_path=f"piadng 10.10.0.1 -n {n}")
    # ping2.start()
    ping1.update()
    time.sleep(4)
    ping1.stop()
    # ping2.stop()
