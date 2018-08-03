from bottle import jinja2_template as template, Bottle, redirect, static_file
from controllers import video

app = Bottle()


@app.route('/static/<file_path:path>')
def static(file_path):
    return static_file(file_path, root='./static')


@app.route('/')
def root():
    return template('ambient', title="ambient display")


@app.route('/ambient')
def ambient(day, time, weather_name, weather, temp, city_name):
    return template('ambient', title="ambient display", day=day, time=time, weather= weather_name, weather_icon=weather,
                    temp=temp, city=city_name)


@app.route('/play')
def play_video(video_name):
    url = video.get_url(video_name)
    return template('play', title="play video", caught_url=url)


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
