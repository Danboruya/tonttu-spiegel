import requests
import json
import routes
import subprocess
from datetime import datetime
from static import keys


DEFAULT_CITY_NAME = "koganei"

class ApplicationStatus:

    def __init__(self):
        self.global_status_id = 0
        _get_weather("koganei", self)

    def set_status(self, sid):
        self.global_status_id = sid

    def get_status(self):
        return self.global_status_id

    def __str__(self):
        if self.global_status_id == 0:
            return "ambient"
        elif self.global_status_id == 1:
            return "playing movie"
        elif self.global_status_id == 2:
            return "display off"
        elif self.global_status_id == 3:
            return "display on"
        else:
            return "Unknown status"


class Ambient:
    def __init__(self):
        self.day = datetime.now().strftime("%A, %b %d")
        self.time = datetime.now().strftime("%I:%M %p")
        self.weather_components = get_weather("koganei")

    def set_weather(self, weather_id, weather_name, temp, city_name):
        self.weather_components[0] = weather_id
        self.weather_components[1] = weather_name
        self.weather_components[2] = temp
        self.weather_components[3] = city_name

    def get_weather(self):
        return [self.weather_components[0], self.weather_components[1],
                self.weather_components[2], self.weather_components[3]]

    def get_day(self):
        return self.day

    def get_time(self):
        return self.time


def print_command(cmd, ignore_word, app):
    cmd = cmd.lstrip(ignore_word)
    app.set_status(0)
    return cmd


def _get_weather(city_name, app):
    api_key = keys.OPEN_WEATHER_API_KEY
    api = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"
    url = api.format(city=city_name, key=api_key)
    response = requests.get(url)
    data = json.loads(response.text)
    weather_id = data["weather"][0]['id']
    weather = data['weather'][0]['main']
    temp = str(data['main']['temp']).split(".")[0] + "°C"
    print(data)
    app.set_status(0)
    return [weather_id, weather, temp, city_name]


def get_weather(city_name):
    api_key = keys.OPEN_WEATHER_API_KEY
    api = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"
    url = api.format(city=city_name, key=api_key)
    response = requests.get(url)
    data = json.loads(response.text)
    weather_id = data["weather"][0]['id']
    weather = data['weather'][0]['main']
    temp = str(data['main']['temp']).split(".")[0] + "°C"
    print(data)
    return [weather_id, weather, temp, city_name]


def actions_help(app):
    app.set_status(0)
    msg = "Here are some things you can ask. For example, \n" \
          "Play developer video \n" \
          "  " \
          "Stop movie \n" \
          "  " \
          "Turn on screen \n" \
          "  " \
          "Turn off screen \n" \
          "  " \
          "And Google assistant built-in commands. \n"
    return msg


# def play_some_videos(app):
#    pass
def reload(ambient, pc, flag):
    if flag:
        pc += 1
        [weather_id, weather_name, temp, city_name] = get_weather(DEFAULT_CITY_NAME)
        if 200 <= weather_id <= 232:
            weather = "Thunderstorm"
        elif 300 <= weather_id <= 321:
            weather = "Drizzle"
        elif 500 <= weather_id <= 531:
            weather = "Rain"
        elif 600 <= weather_id <= 622:
            weather = "Snow"
        elif 700 <= weather_id <= 781:
            weather = "Atmosphere"
        elif weather_id == 800:
            weather = "Clear"
        elif 801 <= weather_id <= 804:
            weather = "Clouds"
        else:
            weather = "Unknown"
        day = ambient.get_day()
        time = ambient.get_time()
        ambient.set_weather(weather_id, weather_name, temp, city_name)
        routes.ambient(day, time, weather_name, weather, temp, city_name)
        return pc
    else:
        day = ambient.get_day()
        time = ambient.get_time()
        [weather_id, weather_name, temp, city_name] = ambient.get_weather(DEFAULT_CITY_NAME)
        routes.ambient(day, time, weather_id, weather_name, temp, city_name)


def play_videos(cmd, r_ignore, app):
    app.set_status(1)
    routes.play()
    msg = "Play {} video from youtube".format(cmd.lstrip("play").rstlip(r_ignore))
    return msg


def stop_videos(app):
    app.set_status(0)
    routes.stop()


def screen_off(app):
    app.set_status(2)
    routes.off()
    msg = "OK. The information screen turn off"
    return msg


def screen_on(app):
    app.set_status(3)
    routes.on()
    msg = "Sure. The information screens turn on."
    return msg


def set_volume(cmd, ignore_word_left, ignore_word_right):
    volume = cmd.lstrip(ignore_word_left).rstlip(ignore_word_right)
    subprocess.call("amixer sset Master {}".format(volume), shell=True)
