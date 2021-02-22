from datetime import datetime, timedelta
from typing import List
from aiohttp import ClientSession
from adhan_scheduler.config_files import config


class PrayerTimes:
    """A simple class to calculate and modify prayer times. Times are calculated
    using the https://aladhan.com/prayer-times-api API service."""
    def __init__(self, school: int = config.SCHOOL, method: int = config.METHOD, offset: List[int] = config.OFFSET):
        self.school = school
        self.method = method
        self.tune = self._tune_prayer_times(offset)

        self.current_date = datetime.now()
        self.base_uri = f"http://api.aladhan.com/v1/timings/{self.current_date.strftime('%d-%m-%Y')}"
        self.loc = None
        self.twilight = None
        self._times = None

        self.params = {
            'school': self.school,
            'method': self.method,
            'tune': self.tune,
        }

    async def _set_location(self):
        """Get your current location based on your ip address"""
        async with ClientSession() as session:
            async with session.get("https://api.letgo.com/api/iplookup.json") as resp:
                if resp.status != 200:
                    raise RuntimeError("Unable to get your current location.")
                body = await resp.json()
                self.loc = {'lat': body['latitude'], 'lon': body['longitude'], 'city': body['city']}

                # Update parameters
                self.params['latitude'] = self.loc['lat']
                self.params['longitude'] = self.loc['lon']

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
            offset = eval(offset) if isinstance(offset, str) else offset

            assert offset.__len__() == 5, \
                "To offset the prayer times you need to pass in 1 value for each prayer " \
                "e.g. [-30, 5, 10, 0, 0] will offset Fajr -30 mins, Duhr + 5 mins, Asr +10 mins. " \
                "In this example the 0 values would make no change to Magrib and Isha"
            for index, value in zip([1, 3, 4, 5, 7], offset):
                tune[index] = tune[index] + value
        return ','.join([str(x) for x in tune])

    async def _calculate_prayer_times(self):
        await self._set_location()

        async with ClientSession() as session:
            async with session.get(self.base_uri, params=self.params) as resp:
                body = await resp.json()
                self._times = body['data']['timings']

                del self._times['Imsak']
                del self._times['Midnight']
                self.twilight = {'sunrise': self._times.pop('Sunrise'), 'sunset': self._times.pop('Sunset')}

    def convert_to_time_object(self, salah: str) -> datetime:
        time = self._times[salah.title().strip()]
        return datetime.strptime(time, "%H:%M")

    async def _setup(self):
        if not self._times:
            await self._calculate_prayer_times()

    async def set_isha_one_hour_after_magrib(self):
        """Sets Isha time to 1 hour after Magrib time"""
        await self._setup()
        hour = self._times['Maghrib'][:2]
        hour = int(hour) + 1
        self._times['Isha'] = f"{hour}{self._times['Maghrib'][2:]}"

    async def set_fajr_x_mins_before_sunrise(self, minuets: int = 45):
        """Set Fajr time to the sunrise time minus a given number of minuets. Default: 45 minuets before sunrise"""
        await self._setup()
        sunrise = datetime.strptime(self.twilight['sunrise'], "%H:%M")
        adjusted_time = sunrise - timedelta(minutes=minuets)
        self._times['Fajr'] = adjusted_time.strftime("%H:%M")

    async def get_times(self, *args) -> dict:
        await self._setup()
        if args:
            _times = []
            for arg in args:
                try:
                    _times.append({arg.title().strip(): self._times[arg.title()]})
                except KeyError as err:
                    raise RuntimeError(f"Salah {arg} does not exist, "
                                       f"please choose from the following: {list(self._times.keys())}") from err
            return {k: v for d in _times for k, v in d.items()}
        return self._times
