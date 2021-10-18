#!/usr/bin/env python3

import tempfile, time, json, sys, subprocess, argparse, os
from subprocess import call

parser = argparse.ArgumentParser(description='Set your pomodoro. The default pomodoro is 25m')
parser.add_argument('-p', type=int, help='Your pomodoro minutes')
parser.add_argument('-l', type=int, help='Set this if you need a few minutes within your pomodoro to do something')
parser.add_argument('-c', nargs='?', const=1, type=int, help='This is used for canceling a running instance. It require no arguments after -c')
args = parser.parse_args()

def get_temp_file():
    return [filename for filename in os.listdir('/tmp/') if filename.startswith('pymor') and filename.endswith('.txt')]

def play_sound(path, time):
    call(['aplay', '-d', str(time), path])
    return

def reading_file(path):
    with open(path, 'r') as file:
        filedata = file.read()
        return filedata

def cancel(path):
    with open(path, 'r') as file:
        filedata = file.read()

    filedata = filedata.replace('true', 'false')

    with open(path, 'w') as file:
      file.write(filedata)

def is_active(word):
    word = word
    if 'true' in word:
        return True
    else:
        return False

def sendmessage(message):
    subprocess.Popen(['notify-send.py', '--replaces-id', '1', '--replaces-process', '1', '-u', 'critical', message])
    return

# If it's running
if get_temp_file() and not args.c:
    # add a time left
    sendmessage('Is already running!')
    exit()
elif get_temp_file() and args.c:
    cancel('/tmp/' + get_temp_file()[0])
    sendmessage('Pomodoro has been canceled!')
    exit()
elif not get_temp_file() and args.c:
    sendmessage('Pomodoro has not been initiated!')
    exit()

temp = tempfile.NamedTemporaryFile(suffix='.txt', prefix='pymor')
file_path = '/tmp/' + get_temp_file()[0]
temp.write(b'active: true')
temp.seek(0)
pomodoro=None
leizure_time=None
should_cancel = args.c

if args.p:
    pomodoro = args.p * 60
else:
    pomodoro = 25 * 60

if args.l:
    leizure_time = pomodoro - args.l * 60


sendmessage('Pomodoro has started')
play_sound('/home/aedigo/Documents/Musics/Pomodoro/pomo-start.wav', 1)
while 0 <= pomodoro:
    pomodoro -= 1
    time.sleep(1) 
    if is_active(reading_file(file_path)) == False:
        sendmessage('Pomodoro was canceled!')
        play_sound('/home/aedigo/Documents/Musics/Pomodoro/pomo-cancel.wav', 1)
        break;

    if pomodoro == leizure_time:
        sendmessage('Back to work!')
        play_sound('/home/aedigo/Documents/Musics/Pomodoro/pomo-start.wav', 1)
       
#    print(temp.name, pomodoro, leizure_time, is_active(reading_file()))
else:
    sendmessage('Done! Nice job!')
    play_sound('/home/aedigo/Documents/Musics/Pomodoro/end.wav', 3)
    temp.close()

