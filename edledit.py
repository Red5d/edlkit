from moviepy.editor import *
import sys, os, re, tempfile, argparse

parser = argparse.ArgumentParser()
parser.add_argument("infile", help="Original input video file.")
parser.add_argument("edlfile", help="EDL file with edit definitions.")
parser.add_argument("outfile", help="Edited video file path/name.")
parser.add_argument("-t", "--threads", type=int, help="Number of CPU threads to use.")
parser.add_argument("-p", "--preset", choices=["ultrafast", "superfast", "fast", "medium", "slow", "superslow"], help="FFMPEG preset to use for optimizing the compression. Defaults to 'medium'.")
parser.add_argument("-b", "--bitrate", help="Video bitrate setting. Auto-detected from original video unless specified. Defaults to '2000k'.")
args = parser.parse_args()

file = open(args.edlfile, 'r')
row = file.readlines()

if args.threads == None:
    threadNum = 2
else:
    threadNum = args.threads

if args.preset == None:
    ffmpegPreset = "medium"
else:
    ffmpegPreset = args.preset

try:
    tmpf = tempfile.NamedTemporaryFile()
    os.system("ffmpeg -i \"%s\" 2> %s" % (args.infile, tmpf.name))
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


if args.bitrate == None:
    print("Using original video bitrate: "+videoBitrate)
else:
    videoBitrate = args.bitrate
    if videoBitrate[-1] != 'k':
        videoBitrate = videoBitrate+'k'


clipNum = 1
global prevTime
prevTime = 0
actionTime = False
clips = VideoFileClip(args.infile).subclip(0,0) #blank 0-time clip

for line in row:
    info = line.split()
    nextTime = float(info[0])
    time2 = float(info[1])
    action = info[2]

    clip = VideoFileClip(args.infile).subclip(prevTime,nextTime)
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
        clip = VideoFileClip(args.infile).subclip(prevTime,nextTime)
        clips = concatenate([clips,clip])
        
    prevTime = nextTime


videoLength = VideoFileClip(args.infile).duration
clip = VideoFileClip(args.infile).subclip(prevTime,videoLength)
print("created ending clip from " + str(prevTime) + " to " + str(videoLength))
clips = concatenate([clips,clip])
clips.write_videofile(args.outfile, codec="libx264", fps=24, bitrate=videoBitrate, audio_bitrate=audioBitrate, threads=threadNum, preset=ffmpegPreset)
