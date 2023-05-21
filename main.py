import os
import subprocess
import threading
import dotenv

dotenv.load_dotenv()
API_TOKEN: str = os.getenv('BOT_TOKEN')
ADMIN_ID: int = int(os.getenv('ADMIN_ID'))


# def main() -> list[threading.Thread]:
#     w = threading.Thread(target=subprocess.run, args=["python.exe wait.py"])
#     t = threading.Thread(target=subprocess.run, args=["python.exe print.py"])
#     return [w, t]
#
#
# if __name__ == "__main__":
#     [thr.start() for thr in main()]

def _run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True)
    # if result.stderr:
    #     raise subprocess.CalledProcessError(
    #         returncode=result.returncode,
    #         cmd=result.args,
    #         stderr=result.stderr
    #     )
    for key, value in result.__dict__.items():
        if key != "stderr":
            print(f"{key} - {value}")
        else:
            print(value.decode())
    return result


_run_command("python.exe print.py")