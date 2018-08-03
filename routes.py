from bottle import jinja2_template as template, Bottle, redirect, static_file
from controllers import application

app = Bottle()


@app.route('/static/<file_path:path>')
def static(file_path):
    return static_file(file_path, root='./static')


@app.route('/')
def root():
    [weather_id, weather_name, temp, city_name, weather_icon] = application.get_weather(application.DEFAULT_CITY_NAME)
    container = {'icon': [weather_icon]}
    return template('ambient', title="ambient display", weather=weather_name, temp=temp,
                    city=city_name, container=container)


@app.route('/play')
def play_video(video_name):
    return template('play', title="play video", name=video_name)


@app.route('/nothing')
def nothing():
    return template('nothing', tilte='ambient nothing')


@app.route('/video/control/play')
def play():
    return redirect('/play')


@app.route('/video/control/stop')
def stop():
    return redirect('/')


@app.route('/nothing/control/off')
def off():
    return redirect('/nothing')


@app.route('/nothing/control/on')
def on():
    return redirect('/')
