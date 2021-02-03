from datetime import datetime, timedelta
import pytest
from adhan_scheduler.get_prayer_times import GetPrayerTimes


@pytest.fixture()
def _api():
    yield GetPrayerTimes()


def test_get_prayer_times(_api):
    assert list(_api.get_prayer_times().keys()) == ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']


def test_offset_prayer_times():
    without_offset = list(GetPrayerTimes().prayer_times.values())
    with_offset = list(GetPrayerTimes(offset=[-10, -10, -10, -10, -10]).prayer_times.values())

    for _wo, _wi in zip(without_offset, with_offset):
        # Manual offset
        _wo = (datetime.strptime(_wo, "%H:%M") - timedelta(minutes=10)).strftime("%H:%M")
        assert _wo == _wi


def test_invalid_salah_name(_api):
    with pytest.raises(RuntimeError) as exec_info:
        _api.get_prayer_time('invalid')
        assert str(exec_info.value) == f"Salah {_api} does not exist, " \
                                       f"please choose from the following: {list(_api.prayer_times.keys())}"


def test_set_isha_one_hour_after_magrib(_api):
    _api.set_isha_one_hour_after_magrib()

    maghrib = _api.prayer_times['Maghrib']
    isha = _api.prayer_times['Isha']

    assert (int(isha[:2]) - int(maghrib[:2])) == 1
    assert maghrib[2:] == isha[2:]


def test_set_fajr_x_mins_before_sunrise(_api):
    _api.set_fajr_x_mins_before_sunrise(60)
    time = (_api.convert_to_time_object('fajr') + timedelta(minutes=60)).strftime("%H:%M")
    assert time == _api.twilight['sunrise']
