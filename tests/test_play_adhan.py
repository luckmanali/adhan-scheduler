from random import choice
import pytest
from adhan_scheduler.play_adhan import get_zone, get_available_zones, play_adhan, play_local, is_amixer_working


@pytest.mark.skipif(not get_available_zones(), reason="Sonos speakers not available to test")
def test_get_speaker():
    zones = get_available_zones()
    player = choice(zones)
    zone = get_zone(player)
    assert zone.player_name == player


def test_get_invalid_speaker():
    with pytest.raises(RuntimeError) as exec_info:
        get_zone('DoesNotExist')
        assert str(exec_info.value).startswith("Cant find Sonos player: 'DoesNotExist'. Available speakers:")


@pytest.mark.skipif(not get_available_zones(), reason="Sonos speakers not available to test")
def test_play_on_sonos():
    zones = get_available_zones()
    player = choice(zones)
    zone = get_zone(player)
    play_adhan(
        zone,
        track_uri="https://soundbible.com/mp3/Chamber%20Decompressing-SoundBible.com-1075404493.mp3",
        volume=10
    )


@pytest.mark.skipif(not is_amixer_working(),
                    reason="Cant seem to get amixer working in the pipeline (missing soundcard)?")
def test_play_with_mplayer():
    class Object:
        speaker = 'mplayer'
        uri = "https://soundbible.com/mp3/Chamber%20Decompressing-SoundBible.com-1075404493.mp3"
        volume = 10

    assert play_local(Object()) == 0


def test_play_local_not_installed():
    class Object:
        speaker = 'omxplayer'
        uri = "https://media.sd.ma/assabile/adhan_3435370/a4ab138564ce.mp3"
        volume = 10

    obj = Object()
    with pytest.raises(RuntimeError) as exec_info:
        play_local(obj)
        assert str(exec_info.value) == f"{obj.speaker} is not installed"
