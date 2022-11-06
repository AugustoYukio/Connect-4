from queue import Queue
from flask import session, request
from flask_socketio import (emit, join_room, leave_room, close_room, rooms, disconnect)
from multiprocessing.managers import SyncManager
try:
    from .factory import create_app
    from .src.entities.model.game_objects import GameRoom
except ImportError:
    from factory import create_app
    from src.entities.model.game_objects import GameRoom

app, ws = create_app(config_name='testing')

SyncManager()

class Lobby(object):
    PLAYERS_IN_LOBBY: Queue = Queue(20)


PLAYERS_IN_LOBBY = Lobby()

lobby = Lobby()


# a short running task that returns immediately


@ws.on('new_player', namespace='/test')
def new_player(data):
    session['receive_count'] = session.get('receive_count', 0) + 1
    PLAYERS_IN_LOBBY.put(request.sid)
    game_room = PLAYERS_IN_LOBBY.get_nowait()
    if game_room is not None:
        game = GameRoom(request.sid)

    if not ():
        # GameRoom(request.sid)
        print(f'Size: {PLAYERS_IN_LOBBY.qsize()}')
        # player_waiting = PLAYERS_IN_LOBBY.get_nowait()
        # print(f'{player_waiting} <-:-> {request.sid}')
        ...
    else:
        PLAYERS_IN_LOBBY.put(request.sid)

    emit('my response',
         {'data': data['data'], 'count': session['receive_count']})


@ws.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


@ws.on('my broadcast event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@ws.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@ws.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@ws.on('close room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@ws.on('my room event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@ws.on('disconnect request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@ws.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@ws.on('disconnect', namespace='/test')
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
    app.run()
