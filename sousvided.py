import mongoengine
import logger
import controller_manager

import flask

app = flask.Flask(__name__)
manager = controller_manager.Manager(is_daemon=True)

@app.route('/start')
def hello_world():
    manager.start_run()
    return 'Started'

@app.route('/stop')
def foo():
    manager.end_run()
    return 'Stopped!'


def db_connect():
    mongoengine.connect('py-souvide-dev')

if __name__ == '__main__':
    db_connect()

    with logger.observers() as loggers:
        manager.loggers = loggers
        app.run(host='0.0.0.0')
