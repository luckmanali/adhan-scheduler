# Adhan-Scheduler
This program is designed to calculate prayer times and then schedule cron jobs 
to play the Adhan. Each cron job will be programmed to play the Adhan either through your 
Sonos speaker(s) or through a generic wired or Bluetooth speaker.

## Setup

### Requirements
* [python3.8+](https://www.python.org/)
* [poetry](https://github.com/python-poetry/poetry)
* cli media player `(optional)`

### Installation
```bash
$ make install
```

### Windows users (coming soon)
A docker images will be available soon [adhan-scheduler]().

## Usage
#### NOTE: You only need to run this program once. All future executions will be done automatically. 

### Sonos speaker(s)
To run this program you need to call main() while passing in the name of the Sonos speaker/zone
as the first argument:
```bash
# replace <speaker-name> with the name of your Sonos speaker
$ main.py <speaker-name>
```

### Local speaker (Bluetooth/wired setup)
If you want to use a generic Bluetooth or wired speaker pass in a CLI Media player as the first argument:
```bash
# example using mplayer --> apt install maplayer -y
$ main.py mplayer

# example using omxplayer --> apt install omxplayer -y
$ main.py omxplayer
```

### Volume settings
If you want to set a specific volume level you can pass this in as an optional argument 
(The volume will default to 60% if this is omitted)
```bash
# play at 100% volume
$ main.py <sono-speaker-name> -v 100

# play at 40% volume
$ main.py <sono-speaker-name> --volume 40

# play at 60% volume (default)
$ main.py <sono-speaker-name>
```

## Config
There are a few variables you can adjust in the adhan_scheduler/config.py file

####  To configure a list of adhans to be played at random add your links to the ADHAN variable
```python
ADHANS = [
    # ADD YOUR ADHAN LINKS HERE ...
    "https://github.com/luckmanali/adhan-collection/blob/main/Masjid%20Al-Haram.mp3?raw=true",
]
```

#### A set of supported CLI media players 
If you want to use a different player please make sure to add it to this list.
```python
# Supported CLI Media Players
CLI_MEDIA_PLAYERS = {
    'mplayer',
    'omxplayer'
}
```

#### Select the school you follow to help get accurate initial results
```python
# 0 for Shafi.
# 1 for Hanafi.
SCHOOL = 1
```

#### The method used to calculate the prayer times
```python
"""
The following calculation methods are supported:
1. Muslim World League
2. Islamic Society of North America
3. Egyptian General Authority of Survey
4. Umm Al-Qura University, Makkah
5. University of Islamic Sciences, Karachi
6. Institute of Geophysics, University of Tehran
7. Shia Ithna-Ashari, Leva Institute, Qum
8. Gulf Region
9. Kuwait
10. Qatar
11. Majlis Ugama Islam Singapura, Singapore
12. Union Organization islamic de France
13. Diyanet İşleri Başkanlığı, Turkey
14. Spiritual Administration of Muslims of Russia

For more details please visit: https://aladhan.com/calculation-methods
"""
METHOD = 1
```

#### If you want to apply an offset to the results to match your local mosque / required calculations
```python
# You can tune the results to match your local mosque using the OFFSET variable.
# Index order: "Fajr, Zhuhr, Asr, Maghrib, Isha"
# Example: OFFSET = [-45, 0, 4, 0, -29]
OFFSET = None
```

## Features
* Automatically calculate prayer times based on your location.
  * Automatically calculates your location by looking up your ip.
* Prayer times can be tuned and customized to match your local mosque / requirements.
* Uses crontab to schedule the adhan (removes automatically).
* Plays static or a random adhan from a configurable list.
* Broadcast customizable announcements (coming soon).
  * For example, it can be used as a reminder 20 minutes before the next prayer starts.
  * This feature must be turned on. (it is disabled by default)
* Each Adhan can have a specified volume level e.g. Fajr adhan can be to 30% while others are at 60%.

## PrayerTimes()

### Initialisation configuration
When initializing the PrayerTimes object class you can provide a few of parameters:

| Parameters    | Description                                                                                     | Type          | Required  |  Default  |
| ------------- |:-----------------------------------------------------------------------------------------------:|:-------------:|:---------:|:---------:|
| `school`      | The school you follow. (0 for Shafi, 1 for Hanafi)                                              | `int`         | `False`   | 1         |
| `method`      | The method used to calculate the prayer times.                                                  | `int`         | `False`   | 1         |
| `offset`      | The offset you want to apply to the results to match your local mosque / required calculations. | `List[int]`   | `False`   | `None`    |

### Use:
```python
api = PrayerTimes(school=1, method=1, offset=None)
```

### An example of the offset parameter

```python
# Original instance without an offset
prayer_times = api.get_times()
print(f"original results\n {prayer_times})

# Create new instance with an offset
offset = PrayerTimes(school=1, method=1, offset=[17, 9, -7, 3, -49])

offset_times = offset.get_times()
print(f"offset results\n {offset_times})
-------------------------------------------------------------------------------------------
>> "original results"
{'Fajr': '05:43', 'Dhuhr': '12:21', 'Asr': '15:07', 'Maghrib': '17:07', 'Isha': '18:59'}

>> "offset results"
{'Fajr': '06:00', 'Dhuhr': '12:30', 'Asr': '15:00', 'Maghrib': '17:10', 'Isha': '18:10'}
```

### get_times()
You can get the prayer times using the get_times() method. 
This method takes an optional number of arguments if you want limit the results.

| Parameters    | Description                                  | Type    | Required  |  Default  |
| ------------- |:--------------------------------------------:|:-------:|:---------:|:---------:|
| `*args`       | The name the prayer(s) you want to query. (If you dont pass in any arguments all prayer times will be returned)   |`str`    | `False`   |           |

#### # Get all prayer times
```python
prayer_times = api.get_times()
print(prayer_times)
-------------------------------------------------------------------------------------------
>> {'Fajr': '05:43', 'Dhuhr': '12:21', 'Asr': '15:07', 'Maghrib': '17:07', 'Isha': '18:59'}
```

#### Get prayer times for Maghrib only
```python
prayer_times = api.get_times('maghrib')
print(prayer_times)
---------------------------------------
>> {'Maghrib': '17:07'}
```

#### Get prayer times for both Fajr and Asr
```python
prayer_times = api.get_times('fajr', 'asr')
print(prayer_times)
-------------------------------------------
>> {'Fajr': '05:43', 'Asr': '15:07'}
```

### set_fajr_x_mins_before_sunrise()
You can update fajr 'x' number of minuets before sunrise. (If you want a late fajr alarm instead of a super early one)

| Parameters    | Description                                                             | Type  | Required  |  Default  |
| ------------- |:-----------------------------------------------------------------------:|:-----:|:---------:|:---------:|
| `minuets`     | The number of minuets before sunrise you want to set the fajr alarm to. |`int`  | `False`   | 45        |

```python
sunrise = api.twilight['sunrise']
print(f"Sunrise is at {sunrise})

api.set_fajr_x_mins_before_sunrise(60)
prayer_times = api.get_times('fajr')
print(prayer_time)
--------------------------------------
>> 'Sunrise is at 07:43'
>> {'Fajr': '06:43'}
```

## Scheduler()
### Initialisation configuration
When initializing the Scheduler class you can provide a couple of parameters:

| Parameters    | Description                                      | Type          | Required  |  Default  |
| ------------- |:------------------------------------------------:|:-------------:|:---------:|:---------:|
| `times`       | The name and time of the job you want to create. |`Dict[str:str]`| `True`    |           |
| `command`     | The command you want to apply to the job.        | `str`         | `True`    |           |

### Use:
```python
scheduler = Scheduler(times={"Echo": "14:30"}, command='echo hello_world')
```

### get_job()
You can get a job by its name using the get_job() method.

| Parameters    | Description                          | Type  | Required  |  Default  |
| ------------- |:------------------------------------:|:-----:|:---------:|:---------:|
| `name`        | The name of the job you want to get. |`str`  | `True`    |           |

```python
job = scheduler.get_job("Echo")
print(job)
-------------------------------------------------------------------
>> {"name": "Echo", "time": "14:30", "command": "echo hello_world"}
```

### schedule_job()
You can create a new job or override an existing one using the schedule_job() method.

| Parameters    | Description                             | Type  | Required  |  Default                         |
| ------------- |:---------------------------------------:|:-----:|:---------:|:--------------------------------:|
| `name`        | The name of the job you want to update. |`str`  | `True`    |                                  |
| `time`        | The new time you want to set.           |`str`  | `True`    |                                  |
| `command`     | The new command you want to set.        |`str`  | `False`   | the original `command` parameter |


```python
scheduler.schedule_job("Echo", "12:00", "echo updated")

job = scheduler.get_job("Echo")
print(job)
---------------------------------------------------------------
>> {"name": "Echo", "time": "12:00", "command": "echo updated"}
```

### remove_job()
You can remove a job by its name using the remove_job() method.

| Parameters    | Description                             | Type  | Required  |  Default  |
| ------------- |:---------------------------------------:|:-----:|:---------:|:---------:|
| `name`        | The name of the job you want to delete. |`str`  | `True`    |           |

```python
scheduler.remove_job("Echo")

job = scheduler.get_job("Echo")
print(job)
-------------------------------
>> None
```

## Example
Below is an example of the program being executed:
```bash
$ crontab -l

$ python main.py "Adhan" --volume 70
***************
Adhan Scheduler
***************
Cron job for 06:58 created successfully
Cron job for 12:21 created successfully
Cron job for 15:07 created successfully
Cron job for 17:07 created successfully
Cron job for 18:59 created successfully
Cron job for 06:58 created successfully
Cron job for 00:00 created successfully

Process finished with exit code 0

$ crontab -l
21 12 * * * python /home/luckmanali/_dev/adhan-scheduler/adhan_scheduler/play_adhan.py Adhan --volume 70 # Dhuhr
7 15 * * * python /home/luckmanali/_dev/adhan-scheduler/adhan_scheduler/play_adhan.py Adhan --volume 70 # Asr
7 17 * * * python /home/luckmanali/_dev/adhan-scheduler/adhan_scheduler/play_adhan.py Adhan --volume 70 # Maghrib
59 18 * * * python /home/luckmanali/_dev/adhan-scheduler/adhan_scheduler/play_adhan.py Adhan --volume 70 # Isha
58 6 * * * python /home/luckmanali/_dev/adhan-scheduler/adhan_scheduler/play_adhan.py Adhan --volume 35 # Fajr
@daily python /home/luckmanali/_dev/adhan-scheduler/adhan_scheduler/main.py Adhan --volume 60' # Adhan Scheduler
```

example of main()
```python
# you can find this code in main.py under the function main.
# please adjust this script to match your requirements.

from scheduler import Scheduler
from prayer_times import PrayerTimes

api = PrayerTimes()  # get prayer times for current date and location
await api.set_fajr_x_mins_before_sunrise(minuets=45)  # reset fajr prayer to 45 mins before sunrise

# set cronjob for all prayers
scheduler = Scheduler(
    times=await api.get_times(),
    command=f'python {getcwd()}/play_adhan.py {args.speaker} --volume {args.volume}'
)

# override cronjob for fajr prayer with the volume lowered to half
scheduler.schedule_job(
    name='Fajr',
    time=scheduler.get_job('Fajr')['time'],
    command=f'python {getcwd()}/play_adhan.py {args.speaker} --volume {int(args.volume / 2)}'
)

# Schedule this script to rerun everyday at midnight
scheduler.schedule_job(
    name="Adhan Scheduler",
    time="00:00",
    command=f"python {getcwd()}/main.py {args.speaker} --volume {int(args.volume)}'"
)
```

## TODO
- [ ] Front end GUI
- [ ] Create preconfigured Raspberry Pi image
- [ ] Include WhatsApp notifications
- [ ] Subscribe to a cloud service instead of using a local build (Sonos users only)
