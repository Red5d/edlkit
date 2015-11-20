#! /usr/bin/env python

import os, sys, curses, edl, time, Stopwatch

def addEdit():
    time1 = float("%.2f" % sw.getElapsedTime())
    estruct.time1.append(time1-1)
    estruct.time2.append(time1-0.5)
    estruct.action.append(1)
    estruct.time1.sort()
    estruct.time2.sort()
    
def showStruct():
    linenum = 0
    while linenum <= len(estruct.time1)-1:
        stdscr.addstr(linenum+2, 58, "                               ")
        stdscr.addstr(linenum+2, 70, str(estruct.time1[linenum]))
        linenum = linenum + 1
        
    stdscr.refresh()
    
def pause_continue():
    if sw.running == True:
        sw.stop()
        stdscr.addstr(5,30,"Paused at "+str(sw.getElapsedTime())+"         ")
    else:
        sw.start()
        stdscr.addstr(5,30,"Running...                         ")
        
    
edlfile = sys.argv[1]
editline = 0

# Open specified edl file. (create it if it doesn't exist)
edlfile_read = open(edlfile, 'a+')
estruct = edl.struct(edlfile_read)
    
sw = Stopwatch.stopwatch()

stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
curses.curs_set(0)
stdscr.keypad(1)

showStruct()

stdscr.addstr(0,2,"EDL Kit: Creator with Timer")
stdscr.addstr(8,2,"Keyboard Controls:")
stdscr.addstr(9,2,"m   Mark an edit time in the video.")
stdscr.addstr(10,2,"p   Pause/continue timer.")
stdscr.addstr(11,2,"w   Write edits to file.         ")
stdscr.addstr(12,2,"q   Write edits to file and exit.")

stdscr.addstr(5,30,"Press 'p' (unpause) to begin.")

key = ''
while key != ord('q'):
    key = stdscr.getch()
    stdscr.refresh()
    if key == ord('m'):
        addEdit()
        showStruct()
    elif key == ord('p'):
        pause_continue()
    elif key == ord('w'):
        edlfile_write = open(edlfile, 'w')
        ewriter = edl.writer(edlfile_write)
        ewriter.write_struct(estruct)
        edlfile_write.close()
        stdscr.addstr(0,68,"Saved")
        stdscr.refresh()


edlfile_write = open(edlfile, 'w')
ewriter = edl.writer(edlfile_write)
ewriter.write_struct(estruct)
edlfile_write.close()        
sw.stop()
curses.endwin()

