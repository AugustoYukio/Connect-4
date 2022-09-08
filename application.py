import os
import secrets
import uuid
from flask import Flask, render_template
from flask import session, request
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, emit
from flask_socketio import join_room, leave_room, \
    close_room, rooms, disconnect
from flask_sqlalchemy import SQLAlchemy

# from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()

template_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'src', 'views', 'templates')
app = Flask(__name__, template_folder=template_path)
app.config['SECRET_KEY'] = secrets.token_urlsafe(45)
# socketio = SocketIO(app, async_mode="eventlet")
# eventlet.monkey_patch()
socketio = SocketIO(app)


# a short running task that returns immediately
@app.route('/')
def home():
    return render_template('index.html', )


@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my broadcast event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my room event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


def run_server():
    import eventlet
    eventlet_socket = eventlet.listen(('localhost', 5000))

    # If provided an SSL argument, use an SSL socket
    ssl_args = ['keyfile', 'certfile', 'server_side', 'cert_reqs',
                'ssl_version', 'ca_certs',
                'do_handshake_on_connect', 'suppress_ragged_eofs',
                'ciphers']

    eventlet.wsgi.server(eventlet_socket, app)
    # eventlet.serve(eventlet_socket, app)


if __name__ == '__main__':
    socketio.run(app, debug=True)
    # wsgi.server(eventlet.listen(('', 8000)), app)
    # run_server()
