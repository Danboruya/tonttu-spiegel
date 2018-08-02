import requests
import json
import static.keys
import routes


class ApplicationStatus:

    def __init__(self):
        self.global_status_id = 0

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


def print_command(cmd, ignore_word, app):
    cmd = cmd.lstrip(ignore_word)
    app.set_status = 0
    return cmd


def get_weather(city_name, app):
    api_key = static.keys.OPEN_WEATHER_API_KEY
    api = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"

    url = api.format(city=city_name, key=api_key)
    response = requests.get(url)
    data = json.loads(response.text)
    print(data)
    app.set_status = 0


# def play_some_videos(app):
#    pass


def play_videos(cmd, app):
    routes.play()


def stop_videos(app):
    routes.stop()


def screen_off(app):
    routes.off()


def screen_on(app):
    routes.on()
