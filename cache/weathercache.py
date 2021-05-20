import requests
from django.conf import settings

from adapter.rediscache import RedisCacheAdapter
from cache.basecachehandler import BaseCacheHandler
from handlers.filehandler import FileHandler


class WeatherCache(BaseCacheHandler):
    BASE_KEY = "weather_data"

    def __init__(self):
        self.value = None
        key = self.BASE_KEY
        super().__init__(key=key, timeout=60 * 30)

    def get_configuration(self):
        _cached_content = RedisCacheAdapter.get(
            self.key, machine_alias=self.machine_alias
        )
        if _cached_content:
            self.value = _cached_content
            return self.value
        else:
            url = settings.WEATHER_API["URL"]
            params = {
                settings.WEATHER_API["PARAMETER_NAMES"]["latitude"]: settings.WEATHER_API["PARAMETER_VALUES"][
                    "latitude"],
                settings.WEATHER_API["PARAMETER_NAMES"]["longitude"]: settings.WEATHER_API["PARAMETER_VALUES"][
                    "longitude"],
                settings.WEATHER_API["PARAMETER_NAMES"]["count"]: settings.WEATHER_API["PARAMETER_VALUES"][
                    "count"],
                settings.WEATHER_API["PARAMETER_NAMES"]["secret_key"]: settings.WEATHER_API["PARAMETER_VALUES"][
                    "secret_key"]
            }

            r = requests.get(url=url, params=params)
            if r.status_code == 200:
                data = r.json()
                weather_data = data.get("list")

                self.value = weather_data
                self.set_configuration(weather_data)
                file_handler = FileHandler(data=weather_data)
                file_handler.delete_excel_file()
                file_handler.create_excel_file()
                return weather_data

            else:
                return []
