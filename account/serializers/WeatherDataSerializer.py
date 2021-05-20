from rest_framework import serializers


class WeatherDataSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        response = {
            "id": instance.get("id", None),
            "name": instance.get("name", None),
            "coord": instance.get("coord", None),
            "main": instance.get("main", None),
            "dt": instance.get("dt", None),
            "wind": instance.get("wind", None),
            "sys": instance.get("sys", None),
            "rain": instance.get("rain", None),
            "snow": instance.get("snow", None),
            "clouds": instance.get("clouds", None),
            "weather": instance.get("weather", None),
        }
        return response
