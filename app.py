import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import redis

app = Flask(__name__)

app.config['SECRET_KEY'] = 'typing-secret'

socketio = SocketIO(
    app,
    message_queue="redis://localhost:6379"
)

@app.route('/')
def index():
    return render_template("index.html")

# Client connects
@socketio.on('connect')
def handle_connect():
    print("User connected")

# Client disconnects
@socketio.on('disconnect')
def handle_disconnect():
    print("User disconnected")

# Typing event
@socketio.on('typing')
def handle_typing(data):
    username = data.get('username')
    print(f"{username} is typing")
    emit(
        "user_typing",
        {"username": username},
        broadcast=True,
        include_self=False
    )

# Stop typing event
@socketio.on('stop_typing')
def handle_stop_typing(data):
    username = data.get('username')
    print(f"{username} stopped typing")
    emit(
        "user_stop_typing",
        {"username": username},
        broadcast=True,
        include_self=False
    )

if __name__ == "__main__":
   socketio.run(app, host="0.0.0.0",debug=True, port=5000)