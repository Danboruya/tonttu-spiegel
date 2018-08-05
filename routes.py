from bottle import jinja2_template as template, Bottle, redirect, static_file
import sys

sys.path.append('./')

from controllers import video
from controllers import application

app = Bottle()


@app.route('/static/<file_path:path>')
def static(file_path):
    return static_file(file_path, root='./static')


@app.route('/')
def root():
    redirect('/ambient/0/none')


@app.route('/ambient/<status>/<video_name>')
def ambient(status, video_name):
    print(status)
    print(video_name)
    if status == None:
        status = 0
    if status == 0:
        path = "/"
    elif status == 1:
        path = "/play/{}".format(video_name)
    else:
        path = "/"

    [weather_id, weather_name, temp, city_name, weather_icon] = application.get_weather(application.DEFAULT_CITY_NAME)
    container = {'icon': [weather_icon]}
    page_info = {'path': [path], 'status': [status]}
    return template('ambient', title="ambient display", weather=weather_name, temp=temp,
                    city=city_name, container=container, is_on_screen=True, page_info=page_info)


@app.route('/play/<video_name>')
#def play_video(status, video_name):
def play_video(video_name):
    # status = 0
    # if status == None:
    #    status = 0
    #if status == 0:
    #    path = "localhost:8080/"
    #elif status == 1:
    #    path = "localhost:8080/play/{}".format(video_name)
    url = video.get_url(video_name)
    # page_info = {'path': [path], 'status': [status]}
    # return template('play', title="play video", caught_url=url, page_infor=page_info)
    return template('play', title="play video", caught_url=url)


@app.route('/nothing')
def nothing():
    return template('nothing', tilte='ambient nothing', is_on_screen=True)


@app.route('/video/control/play/<video_name>')
def play(video_name):
    # play_video(video_name)
    return redirect('/play/{}'.format(video_name))


@app.route('/video/control/stop')
def stop():
    # ambient()
    return redirect('/')


@app.route('/nothing/control/off')
def off():
    nothing()
    # return redirect('/nothing')


@app.route('/nothing/control/on')
def on():
    root(0, "")
    # return redirect('/')
