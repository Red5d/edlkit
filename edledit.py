from moviepy.editor import *
import sys

if len(sys.argv) < 3:
    print(str('Usage: python edledit.py "Video File.mp4" "EDL File.edl" "Edited Video File.mp4"'))
    exit()


file = open(sys.argv[2], 'r')
row = file.readlines()

clipNum = 1
global prevTime
prevTime = 0
actionTime = False
clips = VideoFileClip(sys.argv[1]).subclip(0,0) #blank 0-time clip

for line in row:
    info = line.split()
    nextTime = float(info[0])
    time2 = float(info[1])
    action = info[2]

    clip = VideoFileClip(sys.argv[1]).subclip(prevTime,nextTime)
    clips = concatenate([clips,clip])
    print "created subclip from " + str(prevTime) + " to " + str(nextTime)

    prevTime = nextTime
    nextTime = time2

    if action == "1":
        clip = VideoFileClip(sys.argv[1], audio = False).subclip(prevTime,nextTime)
        clips = concatenate([clips,clip])
        print "created muted subclip from " + str(prevTime) + " to " + str(nextTime)
    elif action == "0":
        print "Muted video." #do nothing (video muted)
    else:
        clip = VideoFileClip(sys.argv[1]).subclip(prevTime,nextTime)
        clips = concatenate([clips,clip])
        
    prevTime = nextTime


videoLength = VideoFileClip(sys.argv[1]).duration
clip = VideoFileClip(sys.argv[1]).subclip(prevTime,videoLength)
print "created ending clip from " + str(prevTime) + " to " + str(videoLength)
clips = concatenate([clips,clip])
clips.to_videofile(sys.argv[3])

