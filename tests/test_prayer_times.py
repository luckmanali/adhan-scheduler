from datetime import datetime, timedelta
import pytest
from adhan_scheduler.prayer_times import PrayerTimes


@pytest.fixture()
def _api():
    yield PrayerTimes()


@pytest.mark.asyncio
async def test_get_prayer_times(_api):
    times = await _api.get_times()
    assert list(times.keys()) == ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']


@pytest.mark.asyncio
async def test_offset_prayer_times(_api):
    times = await _api.get_times()

    api = PrayerTimes(offset=[-10, -10, -10, -10, -10])
    offset_times = await api.get_times()

    for _wo, _wi in zip(list(times.values()), list(offset_times.values())):
        # Manual offset
        _wo = (datetime.strptime(_wo, "%H:%M") - timedelta(minutes=10)).strftime("%H:%M")
        assert _wo == _wi


@pytest.mark.asyncio
async def test_invalid_salah_name(_api):
    with pytest.raises(RuntimeError) as exec_info:
        await _api.get_times('invalid')
        times = await _api.get_times()
        assert str(exec_info.value) == f"Salah {_api} does not exist, " \
                                       f"please choose from the following: {list(times.keys())}"


@pytest.mark.asyncio
async def test_set_isha_one_hour_after_magrib(_api):
    await _api.set_isha_one_hour_after_magrib()

    times = await _api.get_times('Maghrib', 'Isha')
    assert (int(times['Isha'][:2]) - int(times['Maghrib'][:2])) == 1
    assert times['Maghrib'][2:] == times['Isha'][2:]


@pytest.mark.asyncio
async def test_set_fajr_x_mins_before_sunrise(_api):
    await _api.set_fajr_x_mins_before_sunrise(60)
    time = (_api.convert_to_time_object('fajr') + timedelta(minutes=60)).strftime("%H:%M")
    assert time == _api.twilight['sunrise']
