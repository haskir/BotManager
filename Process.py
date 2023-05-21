import threading, subprocess


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
        self.status = "Running"
        self.proc: subprocess

    def start(self) -> threading.Thread:
        try:
            thr = threading.Thread(target=subprocess.run, args=[self.path])

        except Exception as e:
            print(e)
        else:
            self.status = "Running"
            return thr

    def __repr__(self):
        return f"{self.name} with {self.uid} is {self.status}"
