"""
A quick script to get the prayer times for a given set of arguments.
This was created for configuration and testing purposes to help test the
offset required to match your required settings / local mosque.
"""


from argparse import ArgumentParser
from typing import List
from get_prayer_times import GetPrayerTimes


def parse_args():
    """Parse the command line arguments"""
    description = "Schedule the Adhan"
    parser = ArgumentParser(description=description)
    parser.add_argument("school", type=int)
    parser.add_argument("method", type=int)
    parser.add_argument("--offset", type=int, nargs=5, default=[0, 0, 0, 0, 0],
                        help="Must provide exactly 5 values for example --offset -45 10 3 0 29")
    return parser.parse_args()


def check_prayer_times(school: int, method: int, offset: List[int]):
    _api = GetPrayerTimes(school, method, offset)
    return _api.get_prayer_times()


def main():
    args = parse_args()
    prayer_times = check_prayer_times(args.school, args.method, args.offset)
    print(prayer_times)


if __name__ == '__main__':
    main()
