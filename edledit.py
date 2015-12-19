from moviepy.editor import *
import sys, os, re, edl, tempfile, argparse

parser = argparse.ArgumentParser()
parser.add_argument("infile", help="Original input video file.")
parser.add_argument("edlfile", help="EDL file with edit definitions.")
parser.add_argument("outfile", help="Edited video file path/name.")
parser.add_argument("-t", "--threads", type=int, help="Number of CPU threads to use.")
parser.add_argument("-p", "--preset", choices=["ultrafast", "superfast", "fast", "medium", "slow", "superslow"], help="FFMPEG preset to use for optimizing the compression. Defaults to 'medium'.")
parser.add_argument("-b", "--bitrate", help="Video bitrate setting. Auto-detected from original video unless specified. Defaults to '2000k'.")
args = parser.parse_args()

estruct = edl.EDL(args.edlfile)

videoBitrate = ""
audioBitrate = ""

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
    videoBitrate = "2000k"
    audioBitrate = "400k"


if args.bitrate == None:
    print("Using original video bitrate: "+videoBitrate)
else:
    videoBitrate = args.bitrate
    if videoBitrate[-1] != 'k':
        videoBitrate = videoBitrate+'k'

if audioBitrate == "" or audioBitrate == " ":
    audioBitrate = "400k"

clipNum = 1
global prevTime
prevTime = 0
actionTime = False
clips = VideoFileClip(args.infile).subclip(0,0) #blank 0-time clip

for edit in estruct.edits:
    nextTime = float(edit.time1)
    time2 = float(edit.time2)
    action = edit.action

    clip = VideoFileClip(args.infile).subclip(prevTime,nextTime)
    clips = concatenate([clips,clip])
    print("created subclip from " + str(prevTime) + " to " + str(nextTime))

    prevTime = nextTime
    nextTime = time2

    if action == "1":
        # Muting audio only. Create a segment with no audio and add it to the rest.
        clip = VideoFileClip(args.infile, audio = False).subclip(prevTime,nextTime)
        clips = concatenate([clips,clip])
        print("created muted subclip from " + str(prevTime) + " to " + str(nextTime))

        # Advance to next segment time.
        prevTime = nextTime

    elif action == "0":
        #Do nothing (video and audio cut)
        print("Cut video from "+str(prevTime)+" to "+str(nextTime)+".")
        prevTime = nextTime

    elif action == "2":
        # Cut audio and speed up video to cover it.
        v = VideoFileClip(args.infile)

        # Create two clips. One for the cut segment, one immediately after of equal length for use in the speedup.
        s1 = v.subclip(prevTime,nextTime).without_audio()
        s2 = v.subclip(nextTime,(nextTime + s1.duration))

        # Put the clips together, speed them up, and use the audio from the second segment.
        clip = concatenate([s1,s2.without_audio()]).speedx(final_duration=s1.duration).set_audio(s2.audio)
        clips = concatenate([clips,clip])
        print("Cutting audio from "+str(prevTime)+" to "+str(nextTime)+" and squeezing video from "+str(prevTime)+" to "+str(nextTime + s1.duration)+" into that slot.")
        # Advance to next segment time (+time from speedup)
        prevTime = nextTime + s1.duration

    else:
        # No edit action. Just put the clips together and continue.
        clip = VideoFileClip(args.infile).subclip(prevTime,nextTime)
        clips = concatenate([clips,clip])

        # Advance to next segment time.
        prevTime = nextTime


videoLength = VideoFileClip(args.infile).duration
clip = VideoFileClip(args.infile).subclip(prevTime,videoLength)
print("created ending clip from " + str(prevTime) + " to " + str(videoLength))
clips = concatenate([clips,clip])
clips.write_videofile(args.outfile, codec="libx264", fps=24, bitrate=videoBitrate, audio_bitrate=audioBitrate, threads=threadNum, preset=ffmpegPreset)
