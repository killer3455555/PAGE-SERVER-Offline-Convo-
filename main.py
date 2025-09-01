from flask import Flask, request, render_template_string, redirect, url_for, session
import requests
from threading import Thread, Event
import time
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"   # session ke liye zaroori
APP_PASSWORD = "lucifer"     # yahan apna password set karo

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

# 🔹 Stylish Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == APP_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('send_message'))
        else:
            return "<h2 style='color:red;text-align:center;'>❌ Galat Password Nhe lgate cutie</h2><a href='/login'>🔙 phir sa lga sahi password</a>"

    return '''
    <html>
    <head>
        <title>🔐 Secure Login | Muddassir</title>
        <style>
            body {
                background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: #fff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .login-box {
                background: rgba(0,0,0,0.7);
                padding: 30px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 0 25px rgba(0,0,0,0.8);
                animation: fadeIn 1.2s ease-in-out;
            }
            @keyframes fadeIn {
                from {opacity: 0; transform: scale(0.9);}
                to {opacity: 1; transform: scale(1);}
            }
            h1 {
                font-size: 28px;
                margin-bottom: 20px;
                text-shadow: 0 0 10px cyan, 0 0 20px blue;
            }
            input[type="password"] {
                padding: 12px;
                width: 80%;
                border: none;
                border-radius: 8px;
                margin: 10px 0;
                text-align: center;
                font-size: 16px;
            }
            button {
                padding: 12px 25px;
                border: none;
                border-radius: 8px;
                background: cyan;
                font-weight: bold;
                font-size: 16px;
                cursor: pointer;
                transition: 0.3s;
            }
            button:hover {
                background: #00e6e6;
                transform: scale(1.05);
            }
            .links {
                margin-top: 20px;
            }
            .links a {
                display: block;
                margin: 8px 0;
                color: #00ffcc;
                text-decoration: none;
                font-size: 16px;
                transition: 0.3s;
            }
            .links a:hover {
                color: #fff;
                text-shadow: 0 0 10px #00ffcc;
            }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h1>♛ Lord Muddassir Secure Panel ♛</h1>
            <form method="post">
                <input type="password" name="password" placeholder="🔑 Enter Password" required><br>
                <button type="submit">🚀 Login</button>
            </form>
            <div class="links">
                <a href="https://wa.me/923243037456" target="_blank">📲 Connect on WhatsApp</a>
                <a href="https://www.facebook.com/muddassir.OP" target="_blank">🌐 My Facebook Profile</a>
            </div>
        </div>
    </body>
    </html>
    '''

# 🔹 Original Script (Protected)
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
