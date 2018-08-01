from bottle import route, jinja2_template as template, Bottle

app = Bottle()


@app.route('/')
def root():
    return template('ambient', title="ambient display")
