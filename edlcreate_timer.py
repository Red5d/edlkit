#! /usr/bin/env python

import os, sys, curses, edl, time, Stopwatch

def showStruct():
    linenum = 0
    while linenum <= len(estruct.edits)-1:
        stdscr.addstr(linenum+2, 58, "                               ")
        stdscr.addstr(linenum+2, 70, str(estruct.edits[linenum].time1))
        linenum = linenum + 1
        
    stdscr.refresh()
    
def pause_continue():
    if sw.running == True:
        sw.stop()
        stdscr.addstr(5,30,"Paused at "+str("{0:.2f}".format(sw.getElapsedTime()))+"         ")
    else:
        sw.start()
        stdscr.addstr(5,30,"Running...                         ")
        
    
editline = 0

# Open specified edl file. (create it if it doesn't exist)
estruct = edl.EDL(sys.argv[1])
    
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
        time1 = float("%.2f" % sw.getElapsedTime())
        estruct.add("{0:.2f}".format(time1-1), "{0:.2f}".format(time1-0.5), 1)
        showStruct()
    elif key == ord('p'):
        pause_continue()
    elif key == ord('w'):
        estruct.save()
        stdscr.addstr(0,68,"Saved")
        stdscr.refresh()


estruct.save()        
sw.stop()
curses.endwin()

