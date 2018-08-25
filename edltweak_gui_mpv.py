#! /usr/bin/env python

import os, sys, edl, mpv, time
from moviepy.editor import *

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pprint import pprint

num1 = 0
num2 = 0
action2 = 0

playing_original = False
redo_seconds = 0

# Initialize the GUI window
root = Tk()
root.title("EDL Kit: Tweaker")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
    
def updateDisplay(e):
    # Called when the edit selection, edit times, or edit type is changed. Updates the relevant GUI elements.
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

# Set spacing options for the main frame in the GUI.
mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(sticky='nwse')
for column in range(3):
    mainframe.columnconfigure(column, weight=1)
mainframe.rowconfigure(1, weight=1)

# Create an mpv player object and activate the OSD and keyboard/mouse controls.
player = mpv.MPV('osc', 'osd-bar', input_default_bindings=True, input_vo_keyboard=True)
player.keep_open = True

def rewind():
    # "Rewind" the video to either the beginning, or a specified time.
    if redo_seconds == 0:
        player.play('/tmp/tweak.mp4')
        player.pause = False
    else:
        player.time_pos = redo_seconds
        player.pause = False

def play_pause():
    # Toggle play/pause state.
    if player.pause:
        player.pause = False
    else:
        player.pause = True
    
def stop():
    player.quit()

def reload():
    # Reload the video to see the most recent changes.
    player.play('/tmp/tweak.mp4')
    player.pause = False
    global playing_original
    global redo_seconds
    playing_original = False
    redo_seconds = 0

def load_original():
    # Play the original video file.
    player.play(videofile)
    player.pause = False
    global playing_original
    global redo_seconds
    playing_original = True
    redo_seconds = 0

def redo_mark(seconds):
    # Play the original video file starting from a specified time 
    # so an edit can be adjusted while watching the original.
    player.play(videofile)
    global redo_seconds
    redo_seconds = seconds
    player.time_pos = seconds
    player.pause = False
    
def getTime():
    # Get the current video time in seconds.
    return player.time_pos
    

videofile = ""
edlfile = ""
estruct = ""
editline = 0


def videofileset(e):
    # Handle setting a video file when the option is clicked in the GUI.
    global videofile
    videofile = filedialog.askopenfilename()
    if videofile != "":
        videofilevalue.set(videofile.split('/')[-1])

        if edlfile != "":
            show_struct()

def edlfileset(e):
    # Handle setting an EDL file when the option is clicked in the GUI.
    global edlfile
    global estruct
    edlfile = filedialog.askopenfilename()
    if edlfile != "":
        edlfilevalue.set(edlfile.split('/')[-1])
        estruct = edl.EDL(edlfile)

        if videofile != "":
            show_struct()

# Create and set up a frame for the edit time intervals to be displayed.
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

# Create and set up a frame for the edit action to be displayed.
actionLabelFrame = ttk.LabelFrame(mainframe, padding=5, text="Action")
actionLabelFrame.grid(padx=5, pady=5, ipady=2, sticky=(W,N), row=1, column=0)
actionvalue = StringVar()
actionvalue.set("None")
actionlabel = ttk.Label(actionLabelFrame, textvariable=actionvalue, width=30).grid(column=0, row=0, sticky=(E), padx=10)

# Create an set up a frame for the program status to be displayed.
statusLabelFrame = ttk.LabelFrame(root, padding=5, text="Status")
#statusLabelFrame.grid(padx=5, pady=5, ipady=2, sticky=(W), row=2, column=0)
statusLabelFrame.place(x=145, y=145, anchor='c')
statusvalue = StringVar()
statusvalue.set("Ready")
statuslabel = ttk.Label(statusLabelFrame, textvariable=statusvalue, width=30).grid(column=0, row=0, sticky=(E), padx=10)

# Create and set up a frame for the video/EDL filenames to be selected/displayed.
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


# Create and set up a list element for the edits to be displayed in for selection.
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
    # Create a clip of the original video from <start> time to <end> time with <action> applied to the <time1> to <time2> time sub-range.
    v = VideoFileClip(videofile)
    clip1 = v.subclip(start,time1)

    if str(action) == "1":
        if time2 > v.duration:
            end = v.duration
            time2 = end

        clip2 = VideoFileClip(videofile, audio = False).subclip(time1,time2)
        clip3 = v.subclip(time2,end)
        clips = concatenate([clip1,clip2,clip3])
    elif str(action) == "0":
        if time2 > v.duration:
            end = v.duration
            time2 = end

        clip3 = v.subclip(time2,end)
        clips = concatenate([clip1,clip3])
    elif str(action) == "2":
        if time2 > v.duration:
            end = v.duration
            time2 = end
            
        s1 = v.subclip(time1,time2).without_audio()
        s2 = v.subclip(time2, (time2 + s1.duration))
        clip2 = concatenate([s1,s2.without_audio()]).speedx(final_duration=s1.duration).set_audio(s2.audio)
        clip3 = v.subclip((time2 + s1.duration),end)
        clips = concatenate([clip1,clip2,clip3])
    else:
        if time2 > v.duration:
            end = v.duration
            time2 = end

        clips = v.subclip(start,end)
        
    print("Creating clip with modified center from "+str(time1)+" to "+str(time2))
    clips.write_videofile("/tmp/tweak.mp4", codec="libx264", fps=24, preset="ultrafast", threads=4)
    reload()


def show_help():
    # Display a help menu with keyboard controls when the "Keyboard Controls" button is pressed.
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


def show_struct():
    # Display the EDL structure in its element on the GUI.
    linenum = 0
    struct.delete(*struct.get_children())
    while linenum <= len(estruct.edits)-1:
        struct.insert('', 'end', text=str(linenum+1), values=(estruct.edits[linenum].time1, estruct.edits[linenum].time2, estruct.edits[linenum].action))
        linenum = linenum + 1
        
    global num1
    num1 = float(t1value.get())
    global num2    
    num2 = float(t2value.get())
    global action2
    action2 = actionvalue.get()

def update_struct():
    # Called when the EDL structure changes. Updates the relevant GUI elements.
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
    # Handles the keyboard controls.
    key = e.char
    global num1
    global num2
    global action2
    if key == 's':
        # Subtract 0.01 seconds from Time1 
        num1 = num1-0.01
        t1value.set("{0:.2f}".format(num1))
    elif key == 'z':
        # Subtract 0.1 seconds from Time1
        num1 = num1-0.10
        t1value.set("{0:.2f}".format(num1))
    elif key == 'f':
        # Add 0.01 seconds to Time1
        num1 = num1+0.01
        t1value.set("{0:.2f}".format(num1))
    elif key == 'c':
        # Add 0.1 seconds to Time1
        num1 = num1+0.10
        t1value.set("{0:.2f}".format(num1))
    elif key == 'j':
        # Subtract 0.01 seconds from Time2
        num2 = num2-0.01
        t2value.set("{0:.2f}".format(num2))
    elif key == 'm':
        if playing_original:
            # If the original video is playing, mark an edit point at the current time.
            time1 = float(int(getTime()))
            estruct.add(time1-1, time1-0.5, 1)
            show_struct()
        elif redo_seconds != 0:
            # If we're redoing an edit, move the edit point to the current time.
            time1 = float(int(getTime()))
            num1 = time1
            t1value.set("{0:.2f}".format(num1))
            num2 = time1+0.5
            t2value.set("{0:.2f}".format(num2))
        else:
            # If no video is playing, then we're modifying an edit point normally, and will subtract 0.1 seconds from Time2
            num2 = num2-0.10
            t2value.set("{0:.2f}".format(num2))
    elif int(e.keycode) == 119:
        # ("Delete" key) delete an edit point.
        # Remove it from the edit structure...
        estruct.edits.remove([x for x in estruct.edits if float(x.time1) == float(num1)][0])
        # ...and re-display the structure in the GUI
        show_struct()
    elif key == 'l':
        # Add 0.01 seconds to Time2
        num2 = num2+0.01
        t2value.set("{0:.2f}".format(num2))
    elif key == '.':
        # Add 0.1 seconds to Time2
        num2 = num2+0.10
        t2value.set("{0:.2f}".format(num2))
    elif key == '1':
        # Set action to "Mute"
        actionvalue.set("Mute")
        action2 = 1
    elif key == '0':
        # Set action to "Cut"
        actionvalue.set("Cut")
        action2 = 0
    elif key == '2':
        # Set action to "Cut Audio, Speed up video" (speeds up video segment to hide a cut).
        actionvalue.set("Cut audio, Speed up video")
        action2 = 2
    elif key == '-':
        # Set action to "None". Used for when you need to see/hear the original segment during editing.
        actionvalue.set("None")
        action2 = "-"
    elif key == 'r':
        # Re-generate the edited segment and display it.
        statusvalue.set("Reloading Edit...")
        root.update()
        if num1-3 <= 0:
            num1before = 0
        else:
            num1before = num1-3

        if num2+3 >= VideoFileClip(videofile).duration:
            num2after = VideoFileClip(videofile).duration-3
        else:
            num2after = num2+3

        createClip(num1before, num2after, num1, num2, action2)
        statusvalue.set("Ready")
    elif key == 'u':
        # "Rewind" the current video/segment to the beginning.
        rewind()
    elif key == 'p':
        # Toggle pause/play
        play_pause()
    elif key == 'o':
        # Play the original video
        load_original()
    elif key == 'y':
        # Play the original video starting 6 seconds before the current edit point so the edit can be re-marked with "m".
        if int(float(t1value.get()))-6 <= 0:
            redo_mark(0)
        else:
            redo_mark(int(float(t1value.get()))-6)
    elif key == 't':
        # Transfer the modified edit times from the Time Intervals box to the EDL structure, and update the EDL list GUI element.
        item = struct.selection()[0]
        linenum = int(struct.item(item, "text"))-1
        estruct.edits[linenum].time1 = str("{0:.2f}".format(num1))
        estruct.edits[linenum].time2 = str("{0:.2f}".format(num2))
        estruct.edits[linenum].action = str(action2)
        update_struct()
    elif key == 'w':
        # Save (Write) the changed EDL structure to the EDL file.
        estruct.save()
        statusvalue.set("Saved changes.")
    elif key == 'q':
        exit()
        
# GUI action bindings.
# Update the times/action on the GUI when an edit point is selected from the "treeview".
struct.bind('<<TreeviewSelect>>', updateDisplay)

# Handle selecting EDL/video files when the place for that on the GUI is clicked.
edlfilelabel.bind('<Button-1>', edlfileset)
videofilelabel.bind('<Button-1>', videofileset)

# Send keyboard input to the keyCommand function when the window is focused.
root.bind('<Key>', keyCommand)
 
if len(sys.argv) > 1:
    # If run from the cli with video and edl file arguments, go ahead and set those in the gui.
    videofile = sys.argv[1]
    edlfile = sys.argv[2]
    estruct = edl.EDL(edlfile)
    editline = 0
    videofilevalue.set(videofile.split('/')[-1])
    edlfilevalue.set(edlfile.split('/')[-1])
    player.play(videofile.split('/')[-1])
    player.pause = True
    show_struct()

# Set padding options for the GUI elements.
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

# Start the GUI
root.mainloop()
