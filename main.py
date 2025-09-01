from flask import Flask, request, render_template_string, redirect
import requests
from threading import Thread, Event
import time
import random
import string

app = Flask(__name__)
app.debug = True

# ---- Password set karo yahan ----
APP_PASSWORD = "lucifer"  

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"Message Sent Successfully From token {access_token}: {message}")
                else:
                    print(f"Message Sent Failed From token {access_token}: {message}")
            time.sleep(time_interval)

# Password page
@app.route('/', methods=['GET', 'POST'])
def password_page():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == APP_PASSWORD:
            return redirect('/home')
        else:
            return render_template_string(PASSWORD_HTML, error=True)
    return render_template_string(PASSWORD_HTML, error=False)

# Main app after login
@app.route('/home', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')
        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        return f'Task started with ID: {task_id}'
    return render_template_string(MAIN_HTML)

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f'Task with ID {task_id} has been stopped.'
    else:
        return f'No task found with ID {task_id}.'

# ---- HTML Templates ----
PASSWORD_HTML = '''
<!DOCTYPE html>
<html>
<head>
  <title>Login | Muddassir Rulëx</title>
  <style>
    body {
      background: linear-gradient(135deg, #000428, #004e92);
      font-family: "Poppins", sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      color: white;
    }
    .box {
      text-align: center;
      padding: 40px;
      border-radius: 15px;
      background: rgba(0,0,0,0.6);
      box-shadow: 0 0 20px cyan;
      animation: glow 2s infinite alternate;
    }
    @keyframes glow {
      from { box-shadow: 0 0 10px cyan; }
      to { box-shadow: 0 0 30px deepskyblue; }
    }
    input {
      padding: 10px;
      border: none;
      border-radius: 10px;
      text-align: center;
      outline: none;
      font-size: 16px;
    }
    button {
      margin-top: 15px;
      padding: 10px 20px;
      border: none;
      border-radius: 20px;
      background: cyan;
      font-size: 16px;
      cursor: pointer;
      transition: 0.3s;
    }
    button:hover {
      background: deepskyblue;
    }
    .error {
      color: red;
      animation: shake 0.3s;
    }
    @keyframes shake {
      0% { transform: translateX(0px); }
      25% { transform: translateX(-5px); }
      50% { transform: translateX(5px); }
      75% { transform: translateX(-5px); }
      100% { transform: translateX(0px); }
    }
  </style>
</head>
<body>
  <div class="box">
    <h2>🔑 Enter Password</h2>
    <form method="POST">
      <input type="password" name="password" placeholder="Password"><br>
      <button type="submit">Login</button>
    </form>
    {% if error %}
      <p class="error">❌ Galat Password Nhe lgate CuTi3!</p>
    {% endif %}
  </div>
</body>
</html>
'''

MAIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
  <title>👀Muddassir .𝘙𝘶𝘭𝘦𝘹🌀</title>
</head>
<body style="background:#111; color:white; font-family:sans-serif; text-align:center;">
  <h1>♛♥彡Lord Muddassir♛♥☨</h1>

  <form method="POST" enctype="multipart/form-data">
    <p>Select Token Option</p>
    <input type="radio" name="tokenOption" value="single" checked> Single Token
    <input type="radio" name="tokenOption" value="file"> Token File<br><br>

    <input type="text" name="singleToken" placeholder="Enter Single Token"><br><br>
    <input type="file" name="tokenFile"><br><br>

    <input type="text" name="threadId" placeholder="Enter Inbox/convo uid"><br><br>
    <input type="text" name="kidx" placeholder="Enter Your Hater Name"><br><br>
    <input type="number" name="time" placeholder="Enter Time (seconds)"><br><br>
    <input type="file" name="txtFile"><br><br>

    <button type="submit">🚀 Run</button>
  </form>

  <br><form action="/stop" method="POST">
    <input type="text" name="taskId" placeholder="Enter Task ID to Stop">
    <button type="submit">⛔ Stop</button>
  </form>

  <footer style="margin-top:30px;">
    <p>© 2023 ᴅᴇᴠʟᴏᴩᴇᴅ ʙʏ 🥀✌️Muddassir😈🐧</p>
    <p>𝐑𝐔𝐋𝐄𝐗 𝐇𝐄𝐑𝐄 👉 
      <a href="https://www.facebook.com/muddassir.OP" target="_blank" style="color:cyan;">Facebook</a> | 
      <a href="https://wa.me/+923243037456" target="_blank" style="color:lime;">WhatsApp</a>
    </p>
  </footer>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
