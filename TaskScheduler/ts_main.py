from schedule import Scheduler
import time
from pathlib import Path
import json
from subprocess import Popen


def load_json(file: str | Path) -> dict:
    """Loads a JSON file and returns it."""
    with open(file=file,
              mode="r") as f:
        data: dict = json.load(f)

    return data


def health_check(job_name) -> None:
    print(f"Health check:\n"
          f"Current job: {job_name}\n"
          f"Current time: {time.ctime()}\n")


def first_job(to_execute: str | Path) -> None:
    file: Path = Path(to_execute).resolve()
    health_check(job_name="Enlighten Data")

    Popen(
        f"wscript {file}",
        creationflags=0x08000000)


def second_job(to_execute: str | Path) -> None:
    file: Path = Path(to_execute).resolve()
    health_check(job_name="RPA Processing Update")

    Popen(
        f"wscript {file}",
        creationflags=0x08000000)


def run() -> None:
    print(f"Commenced: {time.ctime()}\n")

    scheduler1 = Scheduler()
    scheduler2 = Scheduler()

    files_to_execute: dict = load_json(file=f"{Path.cwd()}/Data/to_execute.json")
    enlighten_data: str = files_to_execute["Enlighten Data"]
    rpa_update: str = files_to_execute["RPA Update"]

    scheduler1.every().day.at("08:00").do(first_job, to_execute=enlighten_data)
    scheduler2.every(15).minutes.do(second_job, to_execute=rpa_update)

    print(scheduler2.idle_seconds)

    while True:
        try:
            scheduler1.run_pending()
            scheduler2.run_pending()
            time.sleep(1)
        except Exception as e:
            print("Below exception raised. Attempting to continue in 10 seconds...")
            print(e)
            time.sleep(10)


if __name__ == '__main__':
    run()
