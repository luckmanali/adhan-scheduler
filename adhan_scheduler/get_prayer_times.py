from datetime import datetime, timedelta
from typing import List
from requests import get
from adhan_scheduler import config


class GetPrayerTimes:
    """A simple class to calculate and modify prayer times. Times are calculated
    using the https://aladhan.com/prayer-times-api API service."""
    def __init__(self, school: int = config.SCHOOL, method: int = config.METHOD, offset: List[int] = config.OFFSET):
        self.school = school
        self.method = method
        self.tune = self._tune_prayer_times(offset)

        self.current_date = datetime.now()
        self.base_uri = f"http://api.aladhan.com/v1/timings/{self.current_date.strftime('%d-%m-%Y')}"
        self.loc = self._get_location()
        self.twilight = None

        self.params = {
            'latitude': self.loc['lat'],
            'longitude': self.loc['lon'],
            'school': self.school,
            'method': self.method,
            'tune': self.tune,
        }

        print(f"\n Getting Prayer Times for {self.loc['city']}")
        self.prayer_times = self._request_prayer_times()

    @staticmethod
    def _get_location() -> dict:
        """Get your current location based on your ip address"""
        data = get('https://api.letgo.com/api/iplookup.json').json()
        return {'lat': data['latitude'], 'lon': data['longitude'], 'city': data['city']}

    @staticmethod
    def _tune_prayer_times(offset: list) -> str:
        """
        Salah   Index
        Fjr     1
        Duhur   3
        Asr     4
        Magrib  5
        Isha    7
        """
        tune = [0] * 9
        # The API returns Magrib at sunset time which is incorrect.
        # So we need to adjust this before continuing.
        tune[5] = 8
        if offset is not None:
            assert offset.__len__() == 5, \
                "To offset the prayer times you need to pass in 1 value for each prayer " \
                "e.g. [-30, 5, 10, 0, 0] will offset Fajr -30 mins, Duhr + 5 mins, Asr +10 mins. " \
                "In this example the 0 values would make no change to Magrib and Isha"
            for index, value in zip([1, 3, 4, 5, 7], offset):
                tune[index] = tune[index] + value

        return ','.join([str(x) for x in tune])

    def _request_prayer_times(self) -> dict:
        resp = get(self.base_uri, params=self.params).json()
        prayer_times = resp['data']['timings']

        del prayer_times['Imsak']
        del prayer_times['Midnight']

        self.twilight = {'sunrise': prayer_times.pop('Sunrise'), 'sunset': prayer_times.pop('Sunset')}
        return prayer_times

    def convert_to_time_object(self, salah: str) -> datetime:
        time = self.prayer_times[salah.title().strip()]
        return datetime.strptime(time, "%H:%M")

    def set_isha_one_hour_after_magrib(self):
        """Sets Isha time to 1 hour after Magrib time"""
        hour = self.prayer_times['Maghrib'][:2]
        hour = int(hour) + 1
        self.prayer_times['Isha'] = f"{hour}{self.prayer_times['Maghrib'][2:]}"

    def set_fajr_x_mins_before_sunrise(self, minuets: int = 45):
        """Set Fajr time to the sunrise time minus a given number of minuets. Default: 45 minuets before sunrise"""
        sunrise = datetime.strptime(self.twilight['sunrise'], "%H:%M")
        adjusted_time = sunrise - timedelta(minutes=minuets)
        self.prayer_times['Fajr'] = adjusted_time.strftime("%H:%M")

    def get_prayer_times(self) -> dict:
        return self.prayer_times

    def get_prayer_time(self, salah: str) -> dict:
        try:
            return {salah.title().strip(): self.prayer_times[salah.title().strip()]}
        except KeyError as err:
            raise RuntimeError(f"Salah {salah} does not exist, "
                               f"please choose from the following: {list(self.prayer_times.keys())}") from err
