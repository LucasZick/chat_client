from flask import Flask, render_template
from flask_socketio import SocketIO, send, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    join_room(username)
    send({'username': 'System', 'message': f'{username} has joined the chat'}, room=username)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    send({'username': username, 'message': message}, broadcast=True)

@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    leave_room(username)
    send({'username': 'System', 'message': f'{username} has left the chat'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=7777)
