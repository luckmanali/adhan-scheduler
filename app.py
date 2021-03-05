import asyncio
from flask import Flask, render_template, request, redirect, jsonify
from adhan_scheduler.prayer_times import PrayerTimes
from adhan_scheduler.scheduler import Scheduler
from adhan_scheduler.play_adhan import get_zone
from datetime import date
from pathlib import Path


app = Flask(__name__)
abs_path = Path(__file__).resolve()

CONFIG = {}


def _init(speaker: str, volume: int = 60):
    prayer_times = PrayerTimes()
    times = asyncio.run(prayer_times.get_times())

    # set cronjob for all prayers
    scheduler = Scheduler(
        times=times,
        command=f'python {abs_path.parent}/adhan_scheduler/play_adhan.py {speaker} --volume {volume}'
    )

    # Schedule this script to rerun everyday at midnight
    scheduler.schedule_job(
        name="Adhan Scheduler",
        time="00:00",
        command=f"python {abs_path.parent}/adhan_scheduler/main.py {speaker} --volume {int(volume)}'"
    )


@app.route('/')
def index():
    scheduler = Scheduler({}, "")
    if scheduler.get_job("Adhan Scheduler") is None:
        # Take me to the setup page
        return render_template("setup.html")

    today = date.today().strftime("%d %b %Y")
    prayer_times = {}
    icons = {}

    for prayer, icon in zip(['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha'],
                            ["wi wi-horizon-alt", "wi wi-day-sunny", "wi wi-day-cloudy", "wi wi-sunset", "wi wi-night-clear"]):
        job = scheduler.get_job(prayer)
        if job:
            _time = job['time'].split(' ')
            _time[0] = (_time[0], f"0{_time[0]}")[len(_time[0]) == 1]
            time = f"{_time[1]}:{_time[0]}"
            prayer_times[job['name']] = time
            icons[job['name']] = icon

    return render_template("index.html", prayer_times=prayer_times, today=today, icons=icons)


@app.route('/setup')
def setup():
    return render_template("setup.html")



@app.route('/process', methods=["POST"])
def process():
    CONFIG['speaker'] = request.form["speaker"]
    CONFIG['volume'] = request.form["volume"]
    try:
        get_zone(CONFIG['speaker'])
    except RuntimeError:
        return jsonify(status=406, success=False, message=f"Sonos speaker {CONFIG['speaker']} not found")
    _init(CONFIG['speaker'], CONFIG['volume'])
    return redirect("/")

@app.route('/toggle', methods=['POST'])
def toggle():
    try:
        scheduler = Scheduler({}, f'python {abs_path.parent}/adhan_scheduler/play_adhan.py {CONFIG["speaker"]} --volume {CONFIG["volume"]}')
    except KeyError:
        return render_template("setup.html")

    if scheduler.get_job(request.form['prayer']):
        scheduler.remove_job(request.form['prayer'])
        return 'disabled'

    prayer_times = PrayerTimes()
    times = asyncio.run(prayer_times.get_times())
    scheduler.schedule_job(request.form['prayer'], times[request.form['prayer']])
    return 'enabled'


if __name__ == '__main__':
    app.run(debug=True)
