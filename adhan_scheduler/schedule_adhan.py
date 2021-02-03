from typing import Optional, Type
from types import TracebackType
from crontab import CronTab


class ScheduleAdhan:
    """Schedule a cron job to play the Adhan for each prayer time"""
    def __init__(self, prayer_times: dict, command: str):
        self.prayer_times = prayer_times
        self.command = command

        self.cron = CronTab(user=True)
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
    def _convert_into_cron_syntax(prayer_time: str) -> str:
        _hour = prayer_time[:2]
        _min = prayer_time[3:5]
        return f"{_min} {_hour} * * *"

    def _remove_all_jobs(self):
        for job in self.cron:
            if job.comment in list(self.prayer_times.keys()):
                self.cron.remove(job)
        self.cron.write()

    def remove_job(self, prayer_name: str):
        for job in self.cron:
            if job.comment == prayer_name.title():
                self.cron.remove(job)
                break
        self.cron.write()

    def schedule_job(self, prayer_name: str, prayer_time: str) -> print:
        cron_time = self._convert_into_cron_syntax(prayer_time)
        job = self.cron.new(command=self.command,
                            comment=prayer_name.title())

        job.setall(cron_time)
        self.cron.write()
        print(f'Cron job for {prayer_time.title()} created successfully')

    def _schedule_all_jobs(self):
        for prayer_name, prayer_time in self.prayer_times.items():
            self.schedule_job(prayer_name, prayer_time)

    def get_job(self, prayer_name: str) -> dict or None:
        for job in self.cron.crons:
            if job.comment == prayer_name.title().strip():
                return {"time": str(job.slices), "command": job.command, "comment": job.comment}
        return None
