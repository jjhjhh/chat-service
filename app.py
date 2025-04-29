from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_socketio import disconnect

app = Flask(__name__)
app.secret_key = 'supersecretkey'
socket_io = SocketIO(app)

users = {}

@app.route("/")
def website():
    return render_template('index.html') 

@app.route("/login", methods=['POST'])
def login():
    id = request.form['id']
    pw = request.form['pw']

    if id == "AdminEunha":
        return render_template('index.html', error='this name is Admin!')

    if id and pw:
        resp = make_response(redirect(url_for('chatting')))
        resp.set_cookie('id', id)
        return resp
    else:
        return render_template('index.html', error='Invalid username or password')

@app.route('/chat')
def chatting():
    username = request.cookies.get('id')
    if username:
        return render_template('chat.html', username=username)
    else:
        return redirect(url_for('website'))


# 연결- 쿠키에서 ID 가져와 저장
@socket_io.on('connect')
def handle_connect():
    id = request.cookies.get('id')
    if id:
        users[request.sid] = id
        print(f"[+] {id} connected")

    else:
        print("[-] No ID found, disconnecting...")
        disconnect()

# 메시지 수신
@socket_io.on('message')
def handle_message(message):
    id = users.get(request.sid, 'Unknown')
    print(f"[{id}] message: {message}")

    if "script" in message:
        return False

    to_client = {
        'message': message,
    }
    send(to_client, broadcast=True)


if __name__ == "__main__":
    socket_io.run(app, host='0.0.0.0', port=5000)
