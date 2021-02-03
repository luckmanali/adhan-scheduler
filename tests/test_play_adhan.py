from random import choice
import pytest
from scripts.play_adhan import get_zone, get_available_zones, play_adhan


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
def test_play_adhan():
    zones = get_available_zones()
    player = choice(zones)
    zone = get_zone(player)
    play_adhan(
        zone,
        track_uri="https://media.sd.ma/assabile/adhan_3435370/a4ab138564ce.mp3",
        volume=10
    )
