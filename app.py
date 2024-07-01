from flask import Flask, render_template, request, redirect, session,url_for
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.secret_key = 'supersecretkey'
socket_io = SocketIO(app)

users = {
    'admin': 'waesrdftygkjf34m40-5j34fmsk',
    'CERT-IS': '1004*',
    'PKNU':'24'
}

# 로그인
@app.route("/")
def website():
    return render_template('index.html') 

@app.route("/login",methods=['GET','POST'])
def login():
    print("login endpoint")
    if request.method=="POST":  #아ㅜㅜ socket_io 추가하면 안 되던 이유가 request가 밑에 함수명이랑 겹쳐서 그런거였음 
        id=request.form['id']
        pw=request.form['pw']
        
        if id in users and users[id]==pw:
            session['id']=id
            return redirect(url_for('chatting'))
        elif id=="admin'-- " or id=="admin'#" or id=="'or 1=1#": #DB를 안 썼더니 SQLinjection이 안 돼서 임의로 열어둠.. ㅁㅊ;;
            session['id']='admin'
            return redirect(url_for('chatting'))
        else:
            return render_template('index.html', error='Invalid username or password')

    return render_template('index.html') 


# 채팅
@app.route('/chat')
def chatting():
    return render_template('chat.html')

@socket_io.on("message")
def request_msg(message):
    print("message : " + message)
    to_client = dict()

    if message == 'new_connect':
        to_client['message'] = "안녕"+session['id']+"."
        to_client['type'] = session['id']
    else:
        to_client['message'] = message
        to_client['type'] = session['id']
    send(to_client, broadcast = True)


if __name__ == "__main__":
    socket_io.run(app, host='0.0.0.0', port=5000)