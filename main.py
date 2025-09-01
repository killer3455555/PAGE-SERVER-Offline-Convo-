from flask import Flask, request, render_template_string, redirect, url_for, session
import requests
from threading import Thread, Event
import time
import random
import string

app = Flask(__name__)
app.secret_key = "super_secret_key"  # session ke liye zaroori
APP_PASSWORD = "Lucifer"    # yahan apna password set karo

# 🔹 Tumhari original headers
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
}

stop_event = Event()

# =============== Stylish Login Page ===============
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == APP_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('send_message'))
        else:
            return '''
            <div style="font-family:sans-serif;text-align:center;margin-top:80px;color:red;">
                <h2>❌ SaHi Password lGa-</h2>
                <a href="/login">🔙 Try Again</a>
            </div>
            '''
    
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>🔐 Secure Login</title>
        <style>
            body {
                margin: 0;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background: linear-gradient(135deg, #1f1c2c, #928DAB);
                font-family: 'Poppins', sans-serif;
                overflow: hidden;
            }
            .login-box {
                background: rgba(255, 255, 255, 0.1);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 8px 32px 0 rgba(0,0,0,0.37);
                backdrop-filter: blur(8px);
                text-align: center;
                animation: fadeIn 1.5s ease-in-out;
            }
            .login-box h2 {
                color: #fff;
                margin-bottom: 20px;
                font-size: 26px;
                letter-spacing: 1px;
                animation: glow 2s infinite alternate;
            }
            .login-box input {
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                border: none;
                border-radius: 10px;
                outline: none;
                font-size: 16px;
            }
            .login-box button {
                margin-top: 15px;
                padding: 12px 20px;
                border: none;
                border-radius: 10px;
                background: linear-gradient(45deg,#00c6ff,#0072ff);
                color: #fff;
                font-size: 16px;
                cursor: pointer;
                transition: 0.3s;
            }
            .login-box button:hover {
                transform: scale(1.05);
                background: linear-gradient(45deg,#ff6a00,#ee0979);
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-30px);}
                to { opacity: 1; transform: translateY(0);}
            }
            @keyframes glow {
                from { text-shadow: 0 0 10px #00f, 0 0 20px #0ff;}
                to { text-shadow: 0 0 20px #ff0, 0 0 30px #f0f;}
            }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h2>🔑 Enter Password</h2>
            <form method="post">
                <input type="password" name="password" placeholder="••••••" required>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    '''

# =============== Tumhari Original Script (protected) ===============
@app.route('/', methods=['GET', 'POST'])
def send_message():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    html_form = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>👀Muddassir .𝘙𝘶𝘭𝘦𝘹🌀</title>
        <style>
            body {font-family: Arial; background:#111; color:#fff; text-align:center;}
            input,textarea {margin:5px; padding:10px; border-radius:8px;}
            button {padding:10px 20px; border-radius:8px; cursor:pointer;}
            footer {margin-top:30px; font-size:14px; color:#aaa;}
        </style>
    </head>
    <body>
        <h1 class="mt-3">♛♥彡Lord Muddassir♛♥☨</h1>
        <form method="post">
            <input type="text" name="url" placeholder="Enter URL" required><br>
            <textarea name="message" placeholder="Enter Message" required></textarea><br>
            <input type="number" name="interval" placeholder="Interval (sec)" value="5"><br>
            <button type="submit">🚀 Start Task</button>
        </form>
        <br>
        <form action="/stop" method="post">
            <button type="submit">🛑 Stop Task</button>
        </form>
        <footer>
            <p>© 2023 ᴅᴇᴠʟᴏᴩᴇᴅ ʙʏ🥀✌️Muddassir😈🐧</p>
        </footer>
    </body>
    </html>
    """

    if request.method == 'POST':
        url = request.form['url']
        message = request.form['message']
        interval = int(request.form['interval'])
        stop_event.clear()
        Thread(target=task, args=(url, message, interval)).start()
        return f"<h2>✅ Task started for {url}</h2><a href='/'>Back</a>"

    return render_template_string(html_form)


@app.route('/stop', methods=['POST'])
def stop():
    stop_event.set()
    return "<h2>🛑 Task stopped</h2><a href='/'>Back</a>"


def task(url, message, interval):
    while not stop_event.is_set():
        try:
            requests.post(url, headers=headers, data={"message": message})
            print(f"✅ Sent: {message}")
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(interval)


if __name__ == '__main__':
    app.run(debug=True)
