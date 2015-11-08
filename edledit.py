from moviepy.editor import *
import sys, os, re, tempfile

if len(sys.argv) < 4:
    print(str('Usage: python edledit.py "Video File.mp4" "EDL File.edl" "Edited Video File.mp4" [threads] [preset] [bitrate]'))
    print(str(''))
    print(str('Threads: Optional. A number between 1 and the number of processor cores you have. Defaults to 2.'))
    print(str('         Determines how many processor cores will be used when creating the edited file.'))
    print(str(''))
    print(str('Preset:  Optional. Changes how well-optimized the compression is. Affects speed and file size, not quality.'))
    print(str('         Choices: ultrafast, superfast, fast, medium, slow, superslow. Defaults to "medium".'))
    print(str(''))
    print(str('Bitrate: Optional. Adjusts the bitrate of the video. Original video bitrate determined automatically.'))
    print(str('         Defaults to "2000k" if automatic detection fails and "bitrate" parameter is not specified.'))
    print(str(''))
    exit()


file = open(sys.argv[2], 'r')
row = file.readlines()

if len(sys.argv) < 5:
    threadNum = 2
else:
    threadNum = sys.argv[4]

if len(sys.argv) < 6:
    ffmpegPreset = "medium"
else:
    ffmpegPreset = sys.argv[5]

try:
    tmpf = tempfile.NamedTemporaryFile()
    os.system("ffmpeg -i \"%s\" 2> %s" % (sys.argv[1], tmpf.name))
    lines = tmpf.readlines()
    tmpf.close()

    for l in lines:
        l = l.strip()
        if l.startswith(b'Duration'):
            videoBitrate = (re.search(b"bitrate: (\d+ kb/s)", l).group(0).split(b':')[1].strip().split(b' ')[0]).decode('utf-8')+"k"

        if l.startswith(b'Stream #0:1'):
            audioBitrate = (re.search(b', (\d+ kb/s)', l).group(1)).strip().split(b' ')[0].decode('utf-8')+"k"

except:
    videoBitrate = str("2000k")
    audiobitrate = str("300k")


if len(sys.argv) == 7:
    videoBitrate = str(sys.argv[6])
else:
    print("Using original video bitrate: "+videoBitrate)


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
    print("created subclip from " + str(prevTime) + " to " + str(nextTime))

    prevTime = nextTime
    nextTime = time2

    if action == "1":
        clip = VideoFileClip(sys.argv[1], audio = False).subclip(prevTime,nextTime)
        clips = concatenate([clips,clip])
        print("created muted subclip from " + str(prevTime) + " to " + str(nextTime))
    elif action == "0":
        print("Muted video.") #do nothing (video muted)
    else:
        clip = VideoFileClip(sys.argv[1]).subclip(prevTime,nextTime)
        clips = concatenate([clips,clip])
        
    prevTime = nextTime


videoLength = VideoFileClip(sys.argv[1]).duration
clip = VideoFileClip(sys.argv[1]).subclip(prevTime,videoLength)
print("created ending clip from " + str(prevTime) + " to " + str(videoLength))
clips = concatenate([clips,clip])
clips.write_videofile(sys.argv[3], codec="libx264", fps=24, bitrate=videoBitrate, audio_bitrate=audioBitrate, threads=threadNum, preset=ffmpegPreset)
