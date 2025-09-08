from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def home():
    return render_template("index.html")

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)

    # Send stored messages from last 7 days
    history = db.get_recent_messages(room)
    for (u, content, ts) in history:
        emit("message", f"[{ts}] {u}: {content}")

    send(f"{username} has entered the room {room}.", to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(f"{username} has left the room {room}.", to=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    msg = data['msg']
    username = data['username']

    db.save_message(room, username, msg)
    send(f"{username}: {msg}", to=room)

if __name__ == "__main__":
    db.init_db()
    socketio.run(app, debug=True)
