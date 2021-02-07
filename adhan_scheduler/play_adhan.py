"""
Description: Play the Adhan through A Sonos speaker(s) or through a connected wired/Bluetooth speaker.

Pre-requisites:
 1. If you are using this script as a stand alone program make sure soco is installed --> pip install soco
 2. You are not using a Sonos speaker then a cli media player is required:
    - omxplayer (recommended for a rasberry pi setup)       --> sudo apt install omxplayer -y
    - mplayer (recommended for linux/mac systems)           --> sudo apt install mplayer -y

Usage:
To run this program you need to call it while passing in the name of the Sonos speaker as the first argument.
If you want to use a Bluetooth or wired speaker pass in omxplayer or mplayer as the first argument instead.
All other arguments are optional.

Arguments:
    speaker (str): the name of the Sonos speaker you want to use                            [[REQUIRED]]
    --volume (int): set the volume percentage (Default is 60%)                              [[OPTIONAL]]
    --uri (str): a uri to the Adhan you want to play (default is random Adhan)              [[OPTIONAL]]
    --help: prints usage and quits the program
"""

from argparse import ArgumentParser
from random import choice
from subprocess import getoutput, run, CalledProcessError
import sys
import soco
from adhan_scheduler.config_files.config import ADHANS, CLI_MEDIA_PLAYERS


def parse_args():
    """Parse the command line arguments"""
    description = "Play a URI through a Sonos or wired/Bluetooth connected speaker"
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
    parser.add_argument('-u', '--uri',
                        nargs='?',
                        default=choice(ADHANS),
                        help='To change the Adhan pass in a custom URI '
                             '(default: a random URI will be selected from the available list in the config)')
    return parser.parse_args()


def get_available_zones() -> list:
    """Get a list of available Sonos speakers"""
    try:
        return [zone_.player_name for zone_ in soco.discovery.discover()]
    except TypeError:
        return []


def get_zone(name: str) -> soco:
    """Return a Sonos Controller for a given speaker"""
    zone = soco.discovery.by_name(name)

    # Check if a zone by the given name was found
    if zone is None:
        zone_names = get_available_zones()
        raise RuntimeError(
            "Cant find Sonos player: '{}'. "
            "Available speakers: \n{}".format(
                name, zone_names
            )
        )

    # Check whether the zone is a coordinator (stand alone zone or
    # master of a group)
    if not zone.is_coordinator:
        raise RuntimeError(
            "The zone '{}' is not a group master, and therefore cannot "
            "play music. Please use '{}' in stead".format(
                name, zone.group.coordinator.player_name
            )
        )
    return zone


def play_adhan(zone: soco, track_uri: str, volume: int):
    """Play the Adhan through a Sonos speaker"""
    zone.volume = volume  # Set volume
    zone.play_uri(track_uri, title="Adhan")  # Play Track at URI


def is_amixer_working():
    """Temp function for pipeline testing"""
    try:
        run(["amixer", "sset", "Master", "10"], check=True)
        return True
    except CalledProcessError:
        return False


def play_local(args) -> int:
    """Play the Adhan through the cli media player"""
    # Get requested player
    player = getoutput(f'which {args.speaker}')

    if player == "":
        raise RuntimeError(f"{player} is not installed")

    # Set the target volume
    run(["amixer", "sset", "Master", f"{args.volume}%"], check=True)

    # Play Adhan
    if player == 'omxplayer':
        process = run([player, "-o", "alsa", args.uri, ">/dev/null 2>&1"], check=True)
    else:
        process = run([player, args.uri], check=True)
    return process.returncode


def main():
    """Start the program"""

    # Settings
    args = parse_args()
    print(
        " Will use the following settings:\n"
        " Speaker: {args.speaker}\n"
        " Volume level: {args.volume}\n"
        " Track: {args.uri}".format(args=args)
    )

    if args.speaker in CLI_MEDIA_PLAYERS:
        play_local(args)
        sys.exit(0)

    zone = get_zone(args.speaker)  # Get Sonos speaker(s)
    play_adhan(zone, track_uri=args.uri, volume=args.volume)


if __name__ == "__main__":
    main()
