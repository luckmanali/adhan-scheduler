from typing import Optional, Type
from types import TracebackType
from crontab import CronTab


class Scheduler:
    """Schedule a cron job"""
    def __init__(self, times: dict, command: str):
        self.times = times
        self.command = command

        self.cron = CronTab(user=True)

        if times != {}:
            self._remove_all_jobs()  # Remove existing jobs (unrelated jobs will not be deleted)
            self._schedule_all_jobs()

    def __enter__(self):
        # For testing purposes
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]):
        # For testing purposes
        self._remove_all_jobs()

    @staticmethod
    def _convert_into_cron_syntax(time: str) -> str:
        _hour = time[:2]
        _min = time[3:5]
        return f"{_min} {_hour} * * *"

    @staticmethod
    def convert_cron_into_str(cron_time: str) -> str:
        _time = cron_time.split(' ')
        time = f"{_time[1]}:{_time[0]}"
        return time

    def _remove_all_jobs(self):
        for job in self.cron:
            if job.comment in list(self.times.keys()):
                self.cron.remove(job)
        self.cron.write()

    def remove_job(self, name: str):
        for job in self.cron:
            if job.comment == name.title():
                self.cron.remove(job)
                break
        self.cron.write()

    def schedule_job(self, name: str, time: str, command: str = None) -> print:
        if not command:
            # Get default
            command = self.command

        # Remove job if it already exists
        self.remove_job(name)

        if "*" not in time:
            time = self._convert_into_cron_syntax(time)

        job = self.cron.new(command=command,
                            comment=name.title())

        job.setall(time)
        self.cron.write()
        print(f'Cron job for {name.title()} at {time} created successfully')

    def _schedule_all_jobs(self):
        for name, time in self.times.items():
            self.schedule_job(name, time)

    def get_job(self, name: str) -> dict or None:
        for job in self.cron.crons:
            if job.comment == name.title().strip():
                return {"name": job.comment, "time": str(job.slices), "command": job.command}
        return None
