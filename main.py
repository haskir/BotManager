import os
import subprocess
import threading


def main() -> list[threading.Thread]:
    w = threading.Thread(target=subprocess.run, args=["python.exe wait.py"])
    t = threading.Thread(target=subprocess.run, args=["python.exe print.py"])
    return [w, t]


if __name__ == "__main__":
    [thr.start() for thr in main()]