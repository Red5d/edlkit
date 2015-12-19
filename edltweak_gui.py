#! /usr/bin/env python

import os, sys, curses, edl, socket, subprocess, time
from moviepy.editor import *

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pprint import pprint

num1 = 0
num2 = 0
action2 = 0

root = Tk()
root.title("EDL Kit: Tweaker")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
    
def updateDisplay(e):
    global num1
    global num2
    global action2
    item = struct.selection()[0]
    t1value.set(float(estruct.edits[int(struct.item(item, "text"))-1].time1))
    num1 = float(t1value.get())
    t2value.set(float(estruct.edits[int(struct.item(item, "text"))-1].time2))
    num2 = float(t2value.get())
    if estruct.edits[int(struct.item(item, "text"))-1].action == "1":
        actionvalue.set("Mute")
        action2 = 1
    elif estruct.edits[int(struct.item(item, "text"))-1].action == "0":
        actionvalue.set("Cut")
        action2 = 0
    elif estruct.edits[int(struct.item(item, "text"))-1].action == "-":
        actionvalue.set("None")
        action2 = "-"
    elif estruct.edits[int(struct.item(item, "text"))-1].action == "2":
        actionvalue.set("Cut audio, Speed up video")
        action2 = 2
    else:
        actionvalue.set("Unknown")
        action2 = "-"



mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(sticky='nwse')
for column in range(3):
    mainframe.columnconfigure(column, weight=1)
mainframe.rowconfigure(1, weight=1)

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

def rewind():
    vlc.send(bytes('prev\n', 'UTF-8'))
    vlc.send(bytes('play\n', 'UTF-8'))
    
def play_pause():
    vlc.send('pause\n'.encode())
    
def stop():
    vlc.send('shutdown\n'.encode())
    vlc.close()

def reload():
    vlc.send('clear\n'.encode())
    vlc.send('add /tmp/tweak.mp4\n'.encode())

def load_original():
    vlc.send('clear\n'.encode())
    vlc.send(('add '+videofile+'\n').encode())    
    
def stdout_on():
    sys.stderr = _stderr
    sys.stdout = _stdout


videofile = ""
edlfile = ""
#edlfile_read = ""
estruct = ""
editline = 0

    

def videofileset(e):
    global videofile
    videofile = filedialog.askopenfilename()
    if videofile != "":
        videofilevalue.set(videofile.split('/')[-1])

        if edlfile != "":
            show_struct()

def edlfileset(e):
    global edlfile
    global estruct
    edlfile = filedialog.askopenfilename()
    if edlfile != "":
        edlfilevalue.set(edlfile.split('/')[-1])
        estruct = edl.EDL(edlfile)

        if videofile != "":
            show_struct()

#stdscr = curses.initscr()
#curses.cbreak()
#curses.noecho()
#curses.curs_set(0)
#stdscr.keypad(1)

intervalLabelFrame = ttk.LabelFrame(mainframe, padding=5, text="Time Intervals")
intervalLabelFrame.grid(padx=5, pady=5, ipady=2, sticky=(W,N), row=0, column=0)
ttk.Label(intervalLabelFrame, text="Time 1: ").grid(column=0, row=0, sticky=(E))
t1value = StringVar()
t1value.set("0.00")
t1label = ttk.Label(intervalLabelFrame, textvariable=t1value, width=12).grid(column=1, row=0, sticky=(W))
ttk.Label(intervalLabelFrame, text="Time 2: ").grid(column=2, row=0, sticky=(E))
t2value = StringVar()
t2value.set("0.00")
t2label = ttk.Label(intervalLabelFrame, textvariable=t2value, width=8).grid(column=3, row=0, sticky=(W))

actionLabelFrame = ttk.LabelFrame(mainframe, padding=5, text="Action")
actionLabelFrame.grid(padx=5, pady=5, ipady=2, sticky=(W,N), row=1, column=0)
actionvalue = StringVar()
actionvalue.set("None")
actionlabel = ttk.Label(actionLabelFrame, textvariable=actionvalue, width=30).grid(column=0, row=0, sticky=(E), padx=10)

statusLabelFrame = ttk.LabelFrame(root, padding=5, text="Status")
#statusLabelFrame.grid(padx=5, pady=5, ipady=2, sticky=(W), row=2, column=0)
statusLabelFrame.place(x=145, y=145, anchor='c')
statusvalue = StringVar()
statusvalue.set("Ready")
statuslabel = ttk.Label(statusLabelFrame, textvariable=statusvalue, width=30).grid(column=0, row=0, sticky=(E), padx=10)

filesLabelFrame = ttk.LabelFrame(root, padding=5, text="Files")
#filesLabelFrame.grid(padx=5, pady=5, sticky=(W,N), row=3, column=0)
filesLabelFrame.place(x=145, y=205, anchor='c')
videofilevalue = StringVar()
videofilelabel = ttk.Label(filesLabelFrame, textvariable=videofilevalue, width=30)
videofilelabel.grid(column=0, row=0, sticky=(W, E), ipadx=10)
videofilevalue.set("<Click to select video file>")

edlfilevalue = StringVar()
edlfilelabel = ttk.Label(filesLabelFrame, textvariable=edlfilevalue, width=30)
edlfilelabel.grid(column=0, row=1, sticky=(W, E, N), ipadx=10)
edlfilevalue.set("<Click to select EDL file>")

struct = ttk.Treeview(mainframe, columns=("Time 1", "Time 2", "Action"), height=20)
struct['show'] = 'headings'
struct.grid(column=1, row=0, rowspan=7)
struct.heading("Time 1", text="Time 1", anchor='center')
struct.column("Time 1", width=70, anchor='center')
struct.heading("Time 2", text="Time 2", anchor='center')
struct.column("Time 2", width=70, anchor='center')
struct.heading("Action", text="Action", anchor='center')
struct.column("Action", width=60, anchor='center')
s = ttk.Scrollbar(struct, orient="vertical", command=struct.yview)
struct.configure(yscrollcommand=s.set)
    

def createClip(start, end, time1, time2, action):
    #print("Action: "+action)

    clip1 = VideoFileClip(videofile).subclip(start,time1)

    if str(action) == "1":
        if time2 > VideoFileClip(videofile).duration:
            end = VideoFileClip(videofile).duration
            time2 = end

        clip2 = VideoFileClip(videofile, audio = False).subclip(time1,time2)
        clip3 = VideoFileClip(videofile).subclip(time2,end)
        clips = concatenate([clip1,clip2,clip3])
    elif str(action) == "0":
        if time2 > VideoFileClip(videofile).duration:
            end = VideoFileClip(videofile).duration
            time2 = end

        clip3 = VideoFileClip(videofile).subclip(time2,end)
        clips = concatenate([clip1,clip3])
    elif str(action) == "2":
        if time2 > VideoFileClip(videofile).duration:
            end = VideoFileClip(videofile).duration
            time2 = end
            
        s1 = VideoFileClip(videofile).subclip(time1,time2).without_audio()
        s2 = VideoFileClip(videofile).subclip(time2, (time2 + s1.duration))
        clip2 = concatenate([s1,s2.without_audio()]).speedx(final_duration=s1.duration).set_audio(s2.audio)
        clip3 = VideoFileClip(videofile).subclip((time2 + s1.duration),end)
        clips = concatenate([clip1,clip2,clip3])
    else:
        if time2 > VideoFileClip(videofile).duration:
            end = VideoFileClip(videofile).duration
            time2 = end

        clips = VideoFileClip(videofile).subclip(start,end)
        

    clips.write_videofile("/tmp/tweak.mp4", codec="libx264", fps=24, preset="ultrafast", threads=2)
    reload()


def show_help():
    helproot = Toplevel(root)
    helpframe = ttk.Frame(helproot, padding="3 3 12 12")
    helpframe.grid(column=0, row=0, sticky=(N, W, E, S))
    helpframe.columnconfigure(0, weight=1)
    helpframe.rowconfigure(0, weight=1)
    ttk.Label(helpframe, text="Keyboard Controls:").grid(column=3, row=8, sticky=(W, E), columnspan=4)
    ttk.Label(helpframe, text="s,f\tMove Time1 left and right by 0.01 seconds.").grid(column=3, row=9, sticky=(W, E), columnspan=4)
    ttk.Label(helpframe, text="z,c\tMove Time1 left and right by 0.10 seconds.").grid(column=3, row=10, sticky=(W, E), columnspan=4)
    ttk.Label(helpframe, text="j,l\tMove Time2 left and right by 0.01 seconds.").grid(column=3, row=11, sticky=(W, E), columnspan=4)
    ttk.Label(helpframe, text="m,.\tMove Time2 left and right by 0.10 seconds.").grid(column=3, row=12, sticky=(W, E), columnspan=4)
    ttk.Label(helpframe, text="1,0,2,-\tSwitch between action 1 (mute), 0 (cut), 2 (cut audio, speed up video), and - (disable).").grid(column=3, row=13, sticky=(W, E), columnspan=4)
    ttk.Label(helpframe, text="t\tTransfer edits to edl structure.").grid(column=3, row=14, sticky=(W, E), columnspan=4)
    ttk.Label(helpframe, text="w\tWrite edits to edl file.").grid(column=3, row=15, sticky=(W, E), columnspan=4)
    ttk.Label(helpframe, text="r\tRecompile edits and display video.").grid(column=3, row=16, sticky=(W, E), columnspan=4)
    ttk.Label(helpframe, text="u,p\tRewind or pause the video.").grid(column=3, row=17, sticky=(W, E), columnspan=4)
    ttk.Label(helpframe, text="o\tPlay the source video file without changes.").grid(column=3, row=18, sticky=(W, E), columnspan=4)
    
ttk.Button(mainframe, text="Keyboard Controls", command=show_help).grid(column=0, row=5)
#stdscr.addstr(5, 30, "Reloading edit...")
#stdscr.refresh()

#stdscr.addstr(0,2,"EDL Kit: Tweaker")
#stdscr.addstr(8,2,"Keyboard Controls:")
#stdscr.addstr(9,2,"s,f    Move Time1 left and right by 0.01 seconds.")
#stdscr.addstr(10,2,"z,c    Move Time1 left and right by 0.10 seconds.")
#stdscr.addstr(11,2,"j,l    Move Time2 left and right by 0.01 seconds.")
#stdscr.addstr(12,2,"m,.    Move Time2 left and right by 0.10 seconds.")
#stdscr.addstr(13,2,"1,0,-  Switch between action 1 (mute), 0 (cut),")
#stdscr.addstr(14,2,"       and - (disable).")
#stdscr.addstr(15,2,"[,]    Move up and down edl file entries.")
#stdscr.addstr(16,2,"       You can also use the arrow keys.")
#stdscr.addstr(17,2,"t      Transfer edits to edl structure.")
#stdscr.addstr(18,2,"w      Write edits to edl file.")
#stdscr.addstr(19,2,"r      Recompile edits and display video.")
#stdscr.addstr(20,2,"u,p    Rewind or pause the video.")
#stdscr.addstr(21,2,"o      Play the source video file without changes.")
#stdscr.addstr(22,2,"q      Quit")

#stdscr.refresh()




def show_struct():
    linenum = 0
    struct.delete(*struct.get_children())
    while linenum <= len(estruct.edits)-1:
        #stdscr.addstr(linenum+2, 58, "                               ")
        #if linenum == editline:
        #    stdscr.addstr(linenum+2, 68, "= "+estruct.time1[linenum]+" "+estruct.time2[linenum]+" "+estruct.action[linenum]+" =")
        struct.insert('', 'end', text=str(linenum+1), values=(estruct.edits[linenum].time1, estruct.edits[linenum].time2, estruct.edits[linenum].action))
        #else:
        #    stdscr.addstr(linenum+2, 70, estruct.time1[linenum]+" "+estruct.time2[linenum]+" "+estruct.action[linenum])

        linenum = linenum + 1
        
    global num1
    num1 = float(t1value.get())
    #num1 = float(estruct.time1[editline])
    global num2    
    num2 = float(t2value.get())
    #num2 = float(estruct.time2[editline])
    global action2
    action2 = actionvalue.get()
    #action2 = str(estruct.action[editline])
    #stdscr.addstr(2, 20, "Time1: "+str(num1)+"    ")
    #stdscr.addstr(2, 40, "Time2: "+str(num2)+"    ")
    
    #if action2 == "1":
    #    stdscr.addstr(5, 30, "Set to mute mode.")
    #elif action2 == "0":
    #    stdscr.addstr(5, 30, "Set to cut mode. ")
    #else:
    #    stdscr.addstr(5, 30, "Set to disabled. ")

#show_struct()


def update_struct():
    struct.set(struct.selection(), column="Time 1", value=t1value.get())
    struct.set(struct.selection(), column="Time 2", value=t2value.get())
    if actionvalue.get() == "Mute":
        struct.set(struct.selection(), column="Action", value="1")
    if actionvalue.get() == "Cut":
        struct.set(struct.selection(), column="Action", value="0")
    if actionvalue.get() == "None":
        struct.set(struct.selection(), column="Action", value="-")
    if actionvalue.get() == "Cut audio, Speed up video":
        struct.set(struct.selection(), column="Action", value="2")


def keyCommand(e):
    key = e.char
    #print(key)
    global num1
    global num2
    global action2
    if key == 's':
        #global num1
        num1 = num1-0.01
        t1value.set("{0:.2f}".format(num1))
    elif key == 'z':
        #global num1
        num1 = num1-0.10
        t1value.set("{0:.2f}".format(num1))
    elif key == 'f':
        #global num1
        num1 = num1+0.01
        t1value.set("{0:.2f}".format(num1))
    elif key == 'c':
        #global num1
        num1 = num1+0.10
        t1value.set("{0:.2f}".format(num1))
    elif key == 'j':
        #global num2
        num2 = num2-0.01
        t2value.set("{0:.2f}".format(num2))
    elif key == 'm':
        #global num2
        num2 = num2-0.10
        t2value.set("{0:.2f}".format(num2))
    elif key == 'l':
        #global num2
        num2 = num2+0.01
        t2value.set("{0:.2f}".format(num2))
    elif key == '.':
        #global num20
        num2 = num2+0.10
        t2value.set("{0:.2f}".format(num2))
    elif key == '1':
        actionvalue.set("Mute")
        #global action2
        action2 = 1
    elif key == '0':
        actionvalue.set("Cut")
        #global action2
        action2 = 0
    elif key == '2':
        actionvalue.set("Cut audio, Speed up video")
        action2 = 2
    elif key == '-':
        actionvalue.set("None")
        #global action2
        action2 = "-"
    elif key == 'r':
        statusvalue.set("Reloading Edit...")
        root.update()
        createClip(num1-3, num2+3, num1, num2, action2)
        statusvalue.set("Ready")
        #if str(action2) == "1":
        #    stdscr.addstr(5, 30, "Set to mute mode.")
        #elif str(action2) == "0":
        #    stdscr.addstr(5, 30, "Set to cut mode. ")
        #else:
        #    stdscr.addstr(5, 30, "Set to disabled. ")
        #stdscr.refresh()        
    elif key == 'u':
        rewind()
    elif key == 'p':
        play_pause()
    elif key == 'o':
        load_original()
    elif key == '[':
        if editline != 0:
            editline = editline-1
            show_struct()
    elif key == ']':
        if editline != len(estruct.edits)-1:
            editline = editline+1
            show_struct()
#    elif key == curses.KEY_UP:
#        if editline != 0:
#            editline = editline-1
#            show_struct()
#    elif key == curses.KEY_DOWN:
#        if editline != len(estruct.time1)-1:
#            editline = editline+1
#            show_struct()
    elif key == 't':
        item = struct.selection()[0]
        linenum = int(struct.item(item, "text"))-1
        estruct.edits[linenum].time1 = str("{0:.2f}".format(num1))
        estruct.edits[linenum].time2 = str("{0:.2f}".format(num2))
        estruct.edits[linenum].action = str(action2)
        update_struct()
    elif key == 'w':
        estruct.save()
        statusvalue.set("Saved changes.")
    elif key == 'q':
        exit()
        
struct.bind('<<TreeviewSelect>>', updateDisplay)
edlfilelabel.bind('<Button-1>', edlfileset)
videofilelabel.bind('<Button-1>', videofileset)
root.bind('<Key>', keyCommand)
 
if len(sys.argv) > 1:
    videofile = sys.argv[1]
    edlfile = sys.argv[2]
    estruct = edl.EDL(edlfile)
    editline = 0
    videofilevalue.set(videofile.split('/')[-1])
    edlfilevalue.set(edlfile.split('/')[-1])
    show_struct()
 
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()

#stop()
#curses.endwin()
