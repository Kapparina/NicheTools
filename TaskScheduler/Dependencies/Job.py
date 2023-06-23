import schedule


class Task:
    Job: callable
    Supervisor: schedule.Scheduler

