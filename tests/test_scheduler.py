from adhan_scheduler.scheduler import Scheduler


def test_schedule_single_job():
    with Scheduler(times={"Asr": "14:30"}, command='echo hello_world') as cron:
        assert cron.get_job("Asr") == {
            'name': 'Asr',
            'time': '30 14 * * *',
            'command': 'echo hello_world',
        }

    # Make sure job has been deleted
    assert cron.get_job("Asr") is None


def test_schedule_multiple_jobs():
    with Scheduler(times={"Maghrib": "17:29", "Isha": "19:00"}, command='echo hello_world') as cron:
        assert cron.get_job("Maghrib") == {
            'name': 'Maghrib',
            'time': '29 17 * * *',
            'command': 'echo hello_world',
        }

        assert cron.get_job("Isha") == {
            'name': 'Isha',
            'time': '0 19 * * *',
            'command': 'echo hello_world',
        }

    # Make sure jobs have been deleted
    assert cron.get_job("Maghrib") is None
    assert cron.get_job("Isha") is None
