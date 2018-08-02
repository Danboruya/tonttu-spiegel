from bottle import jinja2_template as template, Bottle, redirect

app = Bottle()


@app.route('/')
def root():
    return template('ambient', title="ambient display")


@app.route('/play')
def play_video():
    return template('play', title="play video")


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
