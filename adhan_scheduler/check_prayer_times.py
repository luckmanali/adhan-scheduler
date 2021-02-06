"""
A quick script to get the prayer times for a given set of arguments.
This was created for configuration and testing purposes to help test the
settings/offset required to match your required settings / local mosque.
"""


import asyncio
from argparse import ArgumentParser
from typing import List
from prayer_times import PrayerTimes


def parse_args():
    """Parse the command line arguments"""
    description = "Check prayer times"
    parser = ArgumentParser(description=description)
    parser.add_argument("school", type=int)
    parser.add_argument("method", type=int)
    parser.add_argument("--offset", type=int, nargs=5, default=[0, 0, 0, 0, 0],
                        help="Must provide exactly 5 values for example --offset -45 10 3 0 29")
    return parser.parse_args()


async def check_prayer_times(school: int, method: int, offset: List[int]):
    _api = PrayerTimes(school, method, offset)
    return await _api.get_times()


async def main():
    args = parse_args()
    prayer_times = await check_prayer_times(args.school, args.method, args.offset)
    print(prayer_times)


if __name__ == '__main__':
    asyncio.run(main())
