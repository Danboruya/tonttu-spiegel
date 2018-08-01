from bottle import route, run, template, Bottle
from bottle import mako_template as view

app = Bottle()


@app.route('/')
@view('/layouts/application')
def application():
    pass


if __name__ == "__main__":
    run(app=app, host="0.0.0.0", port='8080')
