import requests
import json
import static.keys


def print_command(cmd, ignore_word):
    cmd = cmd.lstrip(ignore_word)
    return cmd


def get_weather(city_name):
    api_key = static.keys.OPEN_WEATHER_API_KEY
    api = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"

    url = api.format(city=city_name, key=api_key)
    response = requests.get(url)
    data = json.loads(response.text)
    print(data)
