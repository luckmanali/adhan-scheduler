"""
This program will schedule a cron job at the beginning time for each prayer.
Each cron job will be programmed to play the Adhan either directly through your
Sonos speaker(s) or through a generic wired or Bluetooth speaker.

Prerequisites (if you do not want to use Sonos):
* A cli media player:
    - omxplayer (recommended for a rasberry pi setup)       --> sudo apt install omxplayer -y
    - mplayer (recommended for linux/mac systems)           --> sudo apt install mplayer -y

Usage:
To run this program you need to call it while passing in the name of the Sonos speaker
as the first argument. e.g. "main.py <sono-speaker-name>"
If you want to use a Bluetooth or wired speaker pass in omxplayer or mplayer as the
first argument instead. e.g. "main.py omxplayer" or "main.py mplayer"

All other arguments are optional.

Arguments:
    speaker (str): the name of the Sonos speaker you want to use                            [[REQUIRED]]
    --volume (int): set the volume percentage (default is 60%)                              [[OPTIONAL]]
    --help: prints usage and quits the program
"""

from os import getcwd
from argparse import ArgumentParser
from schedule_adhan import ScheduleAdhan
from get_prayer_times import GetPrayerTimes


def parse_args():
    """Parse the command line arguments"""
    description = "Schedule the Adhan"
    parser = ArgumentParser(description=description)
    parser.add_argument("speaker",
                        type=str,
                        help="The name of the Sonos speaker/zone you want to use. "
                             "If you want to use a Bluetooth or wired speaker pass in omxplayer or mplayer")
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


def main():
    print_banner('Adhan Scheduler')
    args = parse_args()

    salah = GetPrayerTimes()  # get prayer times for current date and location
    salah.set_fajr_x_mins_before_sunrise(45)  # reset fajr prayer to 45 mins before sunrise

    # set cronjob for all prayers
    ScheduleAdhan(
        prayer_times=salah.prayer_times,
        command=f'python {getcwd()}/play_adhan.py {args.speaker} --volume {args.volume}'
    )

    # override cronjob for fajr prayer with the volume lowered to half
    ScheduleAdhan(
        prayer_times=salah.get_prayer_time('fajr'),
        command=f'python {getcwd()}/play_adhan.py {args.speaker} --volume {int(args.volume / 2)}'
    )


if __name__ == '__main__':
    main()
