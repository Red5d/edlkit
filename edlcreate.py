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
    print "Starting VLC..."
    while testConn > 0:
        testConn = vlc.connect_ex(('127.0.0.1', 12000))
        time.sleep(0.5)
        
else:
    vlc.connect_ex(('127.0.0.1', 12000))
    
    
vlc.recv(2048)

def rewind():
    rwTime = int(getTime())-5
    vlc.send('seek '+str(rwTime)+'\n')
    vlc.recv(2048)
    
def play_pause():
    vlc.send('pause\n')
    vlc.recv(2048)
    
def stop():
    vlc.send('stop\n')
    vlc.close()
    
def getTime():
    vlc.recv(100)
    vlc.send('get_time\n')
    return vlc.recv(100).split('\r')[0]
    
def addEdit():
    time1 = float(int(getTime()))
    estruct.time1.append(str(time1-1))
    estruct.time2.append(str(time1-0.5))
    estruct.action.append(1)
    estruct.time1.sort()
    estruct.time2.sort()
    
def showStruct():
    linenum = 0
    while linenum <= len(estruct.time1)-1:
        stdscr.addstr(linenum+2, 58, "                               ")
        if linenum == editline:
            stdscr.addstr(linenum+2, 68, "= "+estruct.time1[linenum]+" =")
        else:
            stdscr.addstr(linenum+2, 70, estruct.time1[linenum])

        linenum = linenum + 1
        
    stdscr.refresh()
        
        
    
def stdout_on():
    sys.stderr = _stderr
    sys.stdout = _stdout


videofile = sys.argv[1]
vlc.send('add '+videofile+'\n')

edlfile = sys.argv[2]
editline = 0

if os.path.isfile(edlfile):
    edlfile_read = open(edlfile, 'r')
    estruct = edl.struct(edlfile_read)
else:
    estruct = edl.struct()
    

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
        edlfile_write = open(edlfile, 'w')
        ewriter = edl.writer(edlfile_write)
        ewriter.write_struct(estruct)
        edlfile_write.close()
        stdscr.addstr(0,68,"Saved")
        stdscr.refresh()
        
stop()
curses.endwin()

