#! /usr/bin/env python

import os, sys, curses, edl, socket, subprocess, time
from moviepy.editor import *

global num1
num1 = 0
global num2
num2 = 0
global action2
action2 = 0

def stdout_off():
    _stderr = sys.stderr
    _stdout = sys.stdout
    null = open(os.devnull,'wb')
    sys.stdout = sys.stderr = null
    
stdout_off()

try:
    from subprocess import DEVNULL
except ImportError:
#    import os
    DEVNULL = open(os.devnull, 'wb')

vlc = socket.socket()
testConn = vlc.connect_ex(('127.0.0.1', 12000))
if testConn > 0:
    subprocess.Popen(["vlc","-q","--extraintf","rc","--rc-host","localhost:12000"], stdout=DEVNULL, stderr=subprocess.STDOUT)
    print "Starting VLC..."
    while testConn > 0:
        testConn = vlc.connect_ex(('127.0.0.1', 12000))
        time.sleep(0.5)
        
else:
    vlc.connect_ex(('127.0.0.1', 12000))

def rewind():
    vlc.send('prev\n')
    vlc.send('play\n')
    
def play_pause():
    vlc.send('pause\n')
    
def stop():
    vlc.send('stop\n')
    vlc.close()

def reload():
    vlc.send('clear\n')
    vlc.send('add /tmp/tweak.mp4\n')
    
    
def stdout_on():
    sys.stderr = _stderr
    sys.stdout = _stdout


videofile = sys.argv[1]
edlfile = sys.argv[2]
edlfile_read = open(edlfile, 'r')
estruct = edl.struct(edlfile_read)
editline = 0


stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
curses.curs_set(0)
stdscr.keypad(1)
 

def createClip(start, end, time1, time2, action):
    print "Action: "+action

    clip1 = VideoFileClip(videofile).subclip(start,time1)

    if str(action) == "1":
        clip2 = VideoFileClip(videofile, audio = False).subclip(time1,time2)
        clip3 = VideoFileClip(videofile).subclip(time2,end)
        clips = concatenate([clip1,clip2,clip3])
    elif str(action) == "0":
        clip3 = VideoFileClip(videofile).subclip(time2,end)
        clips = concatenate([clip1,clip3])
    else:
        clips = VideoFileClip(videofile).subclip(start,end)
        

    clips.to_videofile("/tmp/tweak.mp4", codec="mpeg4")
    reload()

stdscr.addstr(5, 30, "Reloading edit...")
stdscr.refresh()

stdscr.addstr(0,2,"EDL Kit: Tweaker")
stdscr.addstr(8,2,"Keyboard Controls:")
stdscr.addstr(9,2,"s,f    Move Time1 left and right by 0.01 seconds.")
stdscr.addstr(10,2,"z,c    Move Time1 left and right by 0.10 seconds.")
stdscr.addstr(11,2,"j,l    Move Time2 left and right by 0.01 seconds.")
stdscr.addstr(12,2,"m,.    Move Time2 left and right by 0.10 seconds.")
stdscr.addstr(13,2,"1,0,-  Switch between action 1 (mute), 0 (cut),")
stdscr.addstr(14,2,"       and - (disable).")
stdscr.addstr(15,2,"[,]    Move up and down edl file entries.")
stdscr.addstr(16,2,"       You can also use the arrow keys.")
stdscr.addstr(17,2,"t      Transfer edits to edl structure.")
stdscr.addstr(18,2,"w      Write edits to edl file.")
stdscr.addstr(19,2,"r      Recompile edits and display video.")
stdscr.addstr(20,2,"u,p    Rewind or pause the video.")
stdscr.addstr(21,2,"q      Quit")

stdscr.refresh()




def show_struct():
    linenum = 0
    while linenum <= len(estruct.time1)-1:
        stdscr.addstr(linenum+2, 58, "                               ")
        if linenum == editline:
            stdscr.addstr(linenum+2, 68, "= "+estruct.time1[linenum]+" "+estruct.time2[linenum]+" "+estruct.action[linenum]+" =")
        else:
            stdscr.addstr(linenum+2, 70, estruct.time1[linenum]+" "+estruct.time2[linenum]+" "+estruct.action[linenum])

        linenum = linenum + 1
        
    #global num1
    num1 = float(estruct.time1[editline])
    #global num2    
    num2 = float(estruct.time2[editline])
    #global action2
    action2 = str(estruct.action[editline])
    stdscr.addstr(2, 20, "Time1: "+str(num1)+"    ")
    stdscr.addstr(2, 40, "Time2: "+str(num2)+"    ")
    
    if action2 == "1":
        stdscr.addstr(5, 30, "Set to mute mode.")
    elif action2 == "0":
        stdscr.addstr(5, 30, "Set to cut mode. ")
    else:
        stdscr.addstr(5, 30, "Set to disabled. ")
        
    stdscr.refresh()

show_struct()


stdscr.refresh()

key = ''
while key != ord('q'):
    key = stdscr.getch()
    stdscr.refresh()
    if key == ord('s'):
        #global num1
        num1 = num1-0.01
        stdscr.addstr(2, 20, "Time1: "+str(num1)+"    ")
        stdscr.refresh()
    elif key == ord('z'):
        #global num1
        num1 = num1-0.10
        stdscr.addstr(2, 20, "Time1: "+str(num1)+"    ")
        stdscr.refresh()
    elif key == ord('f'):
        #global num1
        num1 = num1+0.01
        stdscr.addstr(2, 20, "Time1: "+str(num1)+"    ")
        stdscr.refresh()
    elif key == ord('c'):
        #global num1
        num1 = num1+0.10
        stdscr.addstr(2, 20, "Time1: "+str(num1)+"    ")
        stdscr.refresh()
    elif key == ord('j'):
        #global num2
        num2 = num2-0.01
        stdscr.addstr(2, 40, "Time2: "+str(num2)+"    ")
        stdscr.refresh()
    elif key == ord('m'):
        #global num2
        num2 = num2-0.10
        stdscr.addstr(2, 40, "Time2: "+str(num2)+"    ")
        stdscr.refresh()
    elif key == ord('l'):
        #global num2
        num2 = num2+0.01
        stdscr.addstr(2, 40, "Time2: "+str(num2)+"    ")
        stdscr.refresh()
    elif key == ord('.'):
        #global num2
        num2 = num2+0.10
        stdscr.addstr(2, 40, "Time2: "+str(num2)+"    ")
        stdscr.refresh()
    elif key == ord('1'):
        stdscr.addstr(5, 30, "Set to mute mode.")
        #global action2
        action2 = 1
        stdscr.refresh()
    elif key == ord('0'):
        stdscr.addstr(5, 30, "Set to cut mode. ")
        #global action2
        action2 = 0
        stdscr.refresh()
    elif key == ord('-'):
        stdscr.addstr(5, 30, "Set to disabled. ")
        #global action2
        action2 = "-"
        stdscr.refresh()
    elif key == ord('r'):
        stdscr.addstr(5, 30, "Reloading edit...")
        stdscr.refresh()        
        createClip(num1-3, num2+3, num1, num2, action2)
        if str(action2) == "1":
            stdscr.addstr(5, 30, "Set to mute mode.")
        elif str(action2) == "0":
            stdscr.addstr(5, 30, "Set to cut mode. ")
        else:
            stdscr.addstr(5, 30, "Set to disabled. ")
        stdscr.refresh()        
    elif key == ord('u'):
        rewind()
    elif key == ord('p'):
        play_pause()
    elif key == ord('['):
        if editline != 0:
            editline = editline-1
            show_struct()
    elif key == ord(']'):
        if editline != len(estruct.time1)-1:
            editline = editline+1
            show_struct()
    elif key == curses.KEY_UP:
        if editline != 0:
            editline = editline-1
            show_struct()
    elif key == curses.KEY_DOWN:
        if editline != len(estruct.time1)-1:
            editline = editline+1
            show_struct()
    elif key == ord('t'):
        estruct.time1[editline] = str(num1)
        estruct.time2[editline] = str(num2)
        estruct.action[editline] = str(action2)
        stdscr.addstr(0,68,"     ")
        show_struct()
    elif key == ord('w'):
        edlfile_write = open(edlfile, 'w')
        ewriter = edl.writer(edlfile_write)
        ewriter.write_struct(estruct)
        edlfile_write.close()
        stdscr.addstr(0,68,"Saved")
        stdscr.refresh()
        
 
stop()
curses.endwin()
