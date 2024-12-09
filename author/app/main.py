import flask
import os

APP = flask.Flask(__name__)

@APP.route('/')
def index():

    userinfo = {
        'author': os.environ['AUTHOR_NAME'],
        'email' : os.environ['AUTHOR_EMAIL']
    }
    return flask.render_template(
            'index.html', 
            user=userinfo)

if __name__ == '__main__':
    PORT=os.environ['PORT']
    APP.debug = True
    APP.run(host='0.0.0.0', port=PORT)
