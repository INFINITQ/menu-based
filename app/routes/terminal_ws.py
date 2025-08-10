# app/routes/terminal_ws.py  -- REPLACE ENTIRE FILE WITH THIS
from __future__ import annotations

import os
import select
import signal
import threading
import fcntl
import termios
import struct
from typing import Dict

from flask import request, session as flask_session
from flask_socketio import emit, disconnect

from app import socketio

# Keep a map from socket sid -> pty master FD and child PID
_PTY_SESSIONS: Dict[str, Dict] = {}


@socketio.on('connect', namespace='/terminal')
def on_connect():
    # Only allow if Flask session has user
    if 'user' not in flask_session:
        disconnect()
        return
    emit('connected', {'msg': 'connected to terminal namespace'})


@socketio.on('start_shell', namespace='/terminal')
def start_shell(data):
    sid = request.sid
    if sid in _PTY_SESSIONS:
        emit('pty_error', {'error': 'shell already started for this session'})
        return

    master_fd, slave_fd = os.openpty()

    pid = os.fork()
    if pid == 0:
        # child
        os.setsid()
        os.dup2(slave_fd, 0)
        os.dup2(slave_fd, 1)
        os.dup2(slave_fd, 2)
        try:
            os.execv('/bin/bash', ['/bin/bash'])
        except Exception:
            os._exit(1)
    else:
        # parent
        os.close(slave_fd)
        _PTY_SESSIONS[sid] = {'master_fd': master_fd, 'pid': pid}

        t = threading.Thread(target=_pty_reader, args=(sid,), daemon=True)
        t.start()
        emit('pty_started', {'msg': 'shell started'})


def _pty_reader(sid):
    session_info = _PTY_SESSIONS.get(sid)
    if not session_info:
        return
    fd = session_info['master_fd']

    try:
        while True:
            r, _, _ = select.select([fd], [], [], 0.1)
            if fd in r:
                try:
                    data = os.read(fd, 4096)
                    if not data:
                        break
                    # send only to the requesting client
                    socketio.emit('pty_output', {'data': data.decode(errors='ignore')}, to=sid, namespace='/terminal')
                except OSError:
                    break
    finally:
        _cleanup_pty(sid)


@socketio.on('pty_input', namespace='/terminal')
def receive_input(message):
    sid = request.sid
    session_info = _PTY_SESSIONS.get(sid)
    if not session_info:
        emit('pty_error', {'error': 'no active shell'})
        return
    fd = session_info['master_fd']
    data = message.get('data', '')
    if isinstance(data, str):
        data = data.encode()
    try:
        os.write(fd, data)
    except OSError:
        emit('pty_error', {'error': 'write failed'})


@socketio.on('resize', namespace='/terminal')
def handle_resize(message):
    sid = request.sid
    session_info = _PTY_SESSIONS.get(sid)
    if not session_info:
        return
    master_fd = session_info['master_fd']
    cols = int(message.get('cols', 80))
    rows = int(message.get('rows', 24))

    winsize = struct.pack("HHHH", rows, cols, 0, 0)
    fcntl.ioctl(master_fd, termios.TIOCSWINSZ, winsize)


@socketio.on('disconnect', namespace='/terminal')
def on_disconnect():
    sid = request.sid
    _cleanup_pty(sid)


def _cleanup_pty(sid):
    info = _PTY_SESSIONS.pop(sid, None)
    if not info:
        return
    fd = info.get('master_fd')
    pid = info.get('pid')
    try:
        if fd:
            os.close(fd)
    except Exception:
        pass
    try:
        if pid:
            os.kill(pid, signal.SIGHUP)
            # try to reap child to avoid zombie
            try:
                os.waitpid(pid, os.WNOHANG)
            except Exception:
                pass
    except Exception:
        pass
