""" This program is designed to calculate prayer times and then schedule cron jobs to play the Adhan. Each cron job will be programmed to play the Adhan 
either through your Sonos speaker(s) or through a generic wired or Bluetooth speaker.

Prerequisites (if you do not want to use Sonos speaker(s)):
* A cli media player:
    - omxplayer (recommended for a rasberry pi setup)       --> sudo apt install omxplayer -y
    - mplayer (recommended for linux/mac systems)           --> sudo apt install mplayer -y

Usage:
To run this program you need to call it while passing in the name of the Sonos speaker
as the first argument. e.g. "main.py <sono-speaker-name>"
If you want to use a Bluetooth or wired speaker pass in the name of your cli media player as the
first argument instead. e.g. "main.py omxplayer" or "main.py mplayer"

All other arguments are optional.

Arguments:
    speaker (str): the name of the Sonos speaker you want to use                            [[REQUIRED]]
    --volume (int): set the volume percentage (default is 60%)                              [[OPTIONAL]]
    --help: prints usage and quits the program
"""

from pathlib import Path
import asyncio
from argparse import ArgumentParser
from scheduler import Scheduler
from prayer_times import PrayerTimes


def parse_args():
    """Parse the command line arguments"""
    description = "Schedule the Adhan"
    parser = ArgumentParser(description=description)
    parser.add_argument("speaker",
                        type=str,
                        help="The name of the Sonos speaker/zone you want to use. If you want to use a "
                             "Bluetooth or wired speaker pass in the name of your cli media player")
    parser.add_argument('-v', '--volume',
                        nargs='?',
                        default=60,
                        type=int,
                        help='The volume level for the speaker (default is set to 60%)')
    return parser.parse_args()


def print_banner(title: str) -> print:
    """Print out a banner"""
    print('*' * len(title))
    print(title)
    print('*' * len(title))


async def main():
    print_banner('Adhan Scheduler')
    args = parse_args()

    api = PrayerTimes()  # get prayer times for current date and location

    abs_path = Path(__file__).resolve()

    # set cronjob for all prayers
    scheduler = Scheduler(
        times=await api.get_times(),
        command=f'python3 {abs_path.parent}/play_adhan.py {args.speaker} --volume {args.volume} >> cron-out.txt  2>&1'
    )

    # Schedule this script to rerun everyday at midnight
    scheduler.schedule_job(
        name="Adhan Scheduler",
        time="00:00",
        command=f"python3 {abs_path} {args.speaker} --volume {int(args.volume)}"
    )


if __name__ == '__main__':
    asyncio.run(main())
