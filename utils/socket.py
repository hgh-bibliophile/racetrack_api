import socketio
from typing import List

from db import REDIS_URL

class SocketManager:
    def __init__(self, origins: List[str]):
        mgr = socketio.AsyncRedisManager(REDIS_URL)
        self.sio = socketio.AsyncServer(
            client_manager=mgr,
            cors_allowed_origins=origins,
            async_mode="asgi"
        )

        @self.sio.on('connect')
        def connect(sid, environ, auth):
            print('[Connect] ', sid)

        @self.sio.on('disconnect')
        def disconnect(sid):
            print('[Disconnect] ', sid)

        @self.sio.on('watch')
        def watch(sid, data):
            race = data['race']
            self.sio.enter_room(sid, race)
            print('[Watch] (' + race + ')', sid)

    @property
    def emit(self):
        return self.sio.emit

    def merge(self, app):
        return socketio.ASGIApp(self.sio)


