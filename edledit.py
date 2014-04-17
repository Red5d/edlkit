from moviepy.editor import *
import sys

file = open(sys.argv[2], 'r')
row = file.readlines()

clipNum = 1
prevTime = 0
actionTime = False
clips = VideoFileClip(sys.argv[1]).subclip(0,0) #blank 0-time clip

for line in row:
    info = line.split()
    nextTime = float(info[0])
    time2 = float(info[1])
    action = int(info[2])

    clip = VideoFileClip(sys.argv[1]).subclip(prevTime,nextTime)
    clips = concatenate([clips,clip])
    print "created subclip from " + str(prevTime) + " to " + str(nextTime)

    prevTime = nextTime
    nextTime = time2

    if action == 1:
        clip = VideoFileClip(sys.argv[1], audio = False).subclip(prevTime,nextTime)
        clips = concatenate([clips,clip])
        print "created muted subclip from " + str(prevTime) + " to " + str(nextTime)
    else:
        print "Muted video." #do nothing (video muted)
        
    prevTime = nextTime

clips.to_videofile(sys.argv[3])

