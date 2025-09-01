from flask import Flask, request, render_template_string, redirect, url_for, session
import requests
from threading import Thread, Event
import time
import random
import string
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"
PASSWORD = "Lucifer"  # 🔐 Password

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

stop_events = {}
threads = {}

# ================= PASSWORD PROTECT =================
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        pw = request.form.get('password')
        if pw == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('send_message'))
        else:
            return '<h2 style="text-align:center;color:red;margin-top:50px;">❌ Wrong Password</h2><a href="/login" style="text-align:center;display:block;">Try Again</a>'
    return '''
    <html>
    <head>
        <title>🔐 Login</title>
        <style>
            body {background:#111;color:white;font-family:Arial;text-align:center;padding-top:100px;}
            input {padding:10px;margin:10px;border-radius:8px;border:none;}
            button {padding:10px 20px;border-radius:8px;background:linear-gradient(45deg,#00c6ff,#0072ff);color:white;border:none;cursor:pointer;}
        </style>
    </head>
    <body>
        <h2>Enter Password</h2>
        <form method="post">
            <input type="password" name="password" placeholder="••••••" required><br>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    '''

# ================= ORIGINAL SCRIPT =================
@app.route('/', methods=['GET','POST'])
def send_message():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

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

    # ===== HTML exactly as you had, with background, title, WhatsApp, FB link =====
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>👀Muddassir .𝘙𝘶𝘭𝘦𝘹🌀</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
<style>
label { color: white; }
body {background-image:url('https://i.ibb.co/LRrPTkG/c278d531d734cc6fcf79165d664fdee3.jpg');background-size:cover;color:white;}
.container {max-width:350px;border-radius:20px;padding:20px;box-shadow:0 0 15px white;}
.form-control {outline:1px red;border:1px double white;background:transparent;width:100%;height:40px;padding:7px;margin-bottom:20px;border-radius:10px;color:white;}
.header {text-align:center;padding-bottom:20px;}
.btn-submit {width:100%;margin-top:10px;}
.footer {text-align:center;margin-top:20px;color:#888;}
.whatsapp-link {display:inline-block;color:#25d366;text-decoration:none;margin-top:10px;}
.whatsapp-link i {margin-right:5px;}
</style>
</head>
<body>
<header class="header mt-4">
<h1 class="mt-3">♛♥彡Lord Muddassir♛♥☨</h1>
</header>
<div class="container text-center">
<form method="post" enctype="multipart/form-data">
<div class="mb-3">
<label for="tokenOption" class="form-label">Select Token Option</label>
<select class="form-control" id="tokenOption" name="tokenOption" onchange="toggleTokenInput()" required>
<option value="single">Single Token</option>
<option value="multiple">Token File</option>
</select>
</div>
<div class="mb-3" id="singleTokenInput">
<label for="singleToken" class="form-label">Enter Single Token</label>
<input type="text" class="form-control" id="singleToken" name="singleToken">
</div>
<div class="mb-3" id="tokenFileInput" style="display:none;">
<label for="tokenFile" class="form-label">Choose Token File</label>
<input type="file" class="form-control" id="tokenFile" name="tokenFile">
</div>
<div class="mb-3">
<label for="threadId" class="form-label">Enter Inbox/convo uid</label>
<input type="text" class="form-control" id="threadId" name="threadId" required>
</div>
<div class="mb-3">
<label for="kidx" class="form-label">Enter Your Hater Name</label>
<input type="text" class="form-control" id="kidx" name="kidx" required>
</div>
<div class="mb-3">
<label for="time" class="form-label">Enter Time (seconds)</label>
<input type="number" class="form-control" id="time" name="time" required>
</div>
<div class="mb-3">
<label for="txtFile" class="form-label">Choose Your Np File</label>
<input type="file" class="form-control" id="txtFile" name="txtFile" required>
</div>
<button type="submit" class="btn btn-primary btn-submit">Run</button>
</form>
<form method="post" action="/stop">
<div class="mb-3">
<label for="taskId" class="form-label">Enter Task ID to Stop</label>
<input type="text" class="form-control" id="taskId" name="taskId" required>
</div>
<button type="submit" class="btn btn-danger btn-submit mt-3">Stop</button>
</form>
</div>
<footer class="footer">
<p>© 2023 ᴅᴇᴠʟᴏᴩᴇᴅ ʙʏ🥀✌️Muddassir😈🐧</p>
<p>𝐑𝐔𝐋𝐄𝐗 𝐇𝐄𝐑𝐄 <a href="https://www.facebook.com/muddassir.OP">ᴄʟɪᴄᴋ ʜᴇʀᴇ ғᴏʀ ғᴀᴄᴇʙᴏᴏᴋ</a></p>
<a href="https://wa.me/+923243037456" class="whatsapp-link"><i class="fab fa-whatsapp"></i> Chat on WhatsApp</a>
</footer>
<script>
function toggleTokenInput() {
var tokenOption=document.getElementById('tokenOption').value;
if(tokenOption=='single'){document.getElementById('singleTokenInput').style.display='block';document.getElementById('tokenFileInput').style.display='none';}
else{document.getElementById('singleTokenInput').style.display='none';document.getElementById('tokenFileInput').style.display='block';}
}
</script>
</body>
</html>
''')

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f'Task with ID {task_id} has been stopped.'
    else:
        return f'No task found with ID {task_id}.'

# ================= SEND MESSAGES =================
def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for msg in messages:
            if stop_event.is_set(): break
            for token in access_tokens:
                try:
                    api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                    data = {'access_token': token, 'message': f'{mn} {msg}'}
                    r = requests.post(api_url, data=data, headers=headers)
                    if r.status_code == 200:
                        print(f"Message Sent: {msg}")
                    else:
                        print(f"Failed: {msg}")
                except Exception as e:
                    print(f"Error: {e}")
                time.sleep(time_interval)

# ================= RUN SERVER =================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render compatible
    app.run(host='0.0.0.0', port=port)
