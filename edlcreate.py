#! /usr/bin/env python

import os, sys, curses, edl, socket, subprocess, time


def stdout_off():
    _stderr = sys.stderr
    _stdout = sys.stdout
    null = open(os.devnull,'wb')
    sys.stdout = sys.stderr = null
    
#stdout_off()

try:
    from subprocess import DEVNULL
except ImportError:
#    import os
    DEVNULL = open(os.devnull, 'wb')

vlc = socket.socket()
testConn = vlc.connect_ex(('127.0.0.1', 12000))
if testConn > 0:
    subprocess.Popen(["vlc","-q","--extraintf","rc","--rc-host","localhost:12000"], stdout=DEVNULL, stderr=subprocess.STDOUT)
    print("Starting VLC...")
    while testConn > 0:
        testConn = vlc.connect_ex(('127.0.0.1', 12000))
        time.sleep(0.5)
        
else:
    vlc.connect_ex(('127.0.0.1', 12000))
    
    
vlc.recv(2048)

def rewind():
    rwTime = int(getTime())-5
    vlc.send(b"seek "+rwTime.encode('utf-8')+b"\n")
    vlc.recv(2048)
    
def play_pause():
    vlc.send(b"pause\n")
    vlc.recv(2048)
    
def stop():
    vlc.send(b"stop\n")
    vlc.close()

global result    
result = ""
def getTime():
    play_pause()
    play_pause()
    vlc.send(b"get_time\n")
    global result
    result = vlc.recv(100).split(b'\r')
    
    while b'> ' in result[0]:
        vlc.send(b"get_time\n")
        global result
        result = vlc.recv(100).split(b'\r')
    
    if len(result) == 3:
        time = result[1].split(b' ')[1]
    else:
        time = result[0]

    return time
    
    
def addEdit():
    time1 = float(int(getTime()))
    estruct.add(time1-1, time1-0.5, 1)
    estruct.sort()
    
def showStruct():
    linenum = 0
    while linenum <= len(estruct.edits)-1:
        stdscr.addstr(linenum+2, 58, "                               ")
        stdscr.addstr(linenum+2, 70, str(estruct.edits[linenum].time1))
        linenum = linenum + 1
        
    stdscr.refresh()
        
        
    
def stdout_on():
    sys.stderr = _stderr
    sys.stdout = _stdout


videofile = sys.argv[1]
vlc.send(b"add "+videofile.encode('utf-8')+b"\n")

edlfile = sys.argv[2]
editline = 0

# Open specified edl file. (create it if it doesn't exist)
estruct = edl.EDL(edlfile)
    

stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
curses.curs_set(0)
stdscr.keypad(1)

showStruct()

stdscr.addstr(0,2,"EDL Kit: Creator")
stdscr.addstr(8,2,"Keyboard Controls:")
stdscr.addstr(9,2,"m   Mark an edit time in the video.")
stdscr.addstr(10,2,"p   Play/pause video.")
stdscr.addstr(11,2,"u   Rewind video 5 seconds.")
stdscr.addstr(11,2,"w   Write edits to file.         ")
stdscr.addstr(12,2,"q   Write edits to file and exit.")


key = ''
while key != ord('q'):
    key = stdscr.getch()
    stdscr.refresh()
    if key == ord('m'):
        addEdit()
        showStruct()
    elif key == ord('p'):
        play_pause()
    elif key == ord('u'):
        rewind()
    elif key == ord('w'):
        estruct.save()
        stdscr.addstr(0,68,"Saved")
        stdscr.refresh()
        
stop()
curses.endwin()

