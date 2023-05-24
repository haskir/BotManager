import time
from loguru import logger
import subprocess
import threading


class Process:
    LAST = 0
    enc = "cp866"

    @staticmethod
    def __make_filter(name, level):
        def __filter(record):
            return record["extra"].get("name") == name and level == record["level"].name
        return __filter

    def __init__(self, name: str = "",
                 exec_path: str = r"",
                 git: str = r"",
                 uid: int = 0):
        self.name = name
        self.exec_path = exec_path
        self.git = git
        self.log_path = f"log/{name}.log"
        self.error_path = f"log/{name}_error.log"
        if not uid:
            self.uid = self.LAST
            self.__class__.LAST += 1
        self.status: str = "Stopped"
        self.__stop = False
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
        self._log.info(string.rstrip("\n"))
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
        self.status = "running"
        self.on_start()

    def stop(self):
        self.__stop = True
        self.__process.send_signal(0)
        self.status = "stopped"
        self.on_stop()

    def restart(self):
        self.stop()
        self.start()

    def update(self):
        self.stop()
        updater = subprocess.Popen(f"git pull {self.exec_path}", stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
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

    def __start_proc(self) -> subprocess.Popen:
        return subprocess.Popen(self.exec_path,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True,
                                encoding=self.enc,
                                errors='replace')

    def __logging(self):
        while not self.__stop:
            try:
                output = self.__process.stdout.readline()
                if output == '' and self.__process.poll() is not None:
                    self.status = "stopped"
                    break
                if output:
                    self.on_log(output)
            except AttributeError:
                ...
        [self.on_error(error) for error in self.__process.stderr.readlines() if error]

    def __repr__(self):
        return f"{self.name} with {self.uid} uid is {self.status}"


if __name__ == "__main__":
    n = 20
    ping1 = Process(name="Ping1", exec_path=f"ping 1.1.1.1 -n {n}")
    ping1.start()

    # ping2 = Process(name="Ping2", exec_path=f"piadng 10.10.0.1 -n {n}")
    # ping2.start()
    #
    time.sleep(4)
    #
    ping1.stop()
    # ping2.stop()

    # ping1.update()
