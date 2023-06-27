import schedule
import time
from pathlib import Path
from datetime import datetime, timedelta
import json
from subprocess import Popen
import os


CURRENT_TIME: str = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
TIME_FORMAT: str = "%d/%m/%Y - %H:%M:%S"


def load_json(file: str | Path) -> dict:
    """Loads a JSON file and returns it."""
    with open(file=file,
              mode="r") as f:
        data: dict = json.load(f)

    return data


def health_check(job_name) -> None:
    print(f"---- Health check ----\n"
          f"Current job: {job_name}\n"
          f"Job commencement time: {datetime.now().strftime(TIME_FORMAT)}\n")


def first_job(to_execute: str | Path) -> None:
    os.system("cls")
    file: Path = Path(to_execute).resolve()
    health_check(job_name="Enlighten Data")

    Popen(
        f"wscript {file}",
        creationflags=0x08000000)


def second_job(to_execute: str | Path) -> None:
    os.system("cls")
    file: Path = Path(to_execute).resolve()
    health_check(job_name="RPA Processing Update")

    Popen(
        f"wscript {file}",
        creationflags=0x08000000)


def run() -> None:
    print(f"Scheduling commenced: {CURRENT_TIME}\n")

    files_to_execute: dict = load_json(file=f"{Path.cwd()}/Data/to_execute.json")
    enlighten_data: str = files_to_execute["Enlighten Data"]
    rpa_update: str = files_to_execute["RPA Update"]

    schedule.every().day.at("08:00").do(
        job_func=first_job,
        to_execute=enlighten_data)

    schedule.every(2).hours.at(":00").do(
        job_func=second_job,
        to_execute=rpa_update)

    while True:
        try:
            schedule.run_pending()
            wait_time: float = schedule.idle_seconds()
            print(f"Next job at: {(datetime.now() + timedelta(seconds=wait_time)).strftime(TIME_FORMAT)}")
            time.sleep(wait_time)
        except Exception as e:
            print("Below exception raised. Attempting to continue in 10 seconds...")
            print(e)
            time.sleep(10)


if __name__ == '__main__':
    run()
