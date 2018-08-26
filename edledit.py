from moviepy.editor import *
import sys, os, re, edl, tempfile, argparse
from pymediainfo import MediaInfo

def render(videofile, estruct, outfile, videoBitrate="2000k", audioBitrate="400k", threadNum=2, ffmpegPreset="medium", vcodec=None, acodec=None, ffmpeg_params=None, writeLogfile=False):
    clipNum = 1
    global prevTime
    prevTime = 0
    actionTime = False
    v = VideoFileClip(videofile)
    duration = v.duration
    clips = v.subclip(0,0) #blank 0-time clip

    for edit in estruct.edits:
        nextTime = float(edit.time1)
        time2 = float(edit.time2)
        action = edit.action

        if nextTime > duration:
            nextTime = duration

        if prevTime > duration:
            prevTime = duration

        clip = v.subclip(prevTime,nextTime)
        clips = concatenate([clips,clip])
        print("created subclip from " + str(prevTime) + " to " + str(nextTime))

        prevTime = nextTime
        nextTime = time2

        if action == "1":
            # Muting audio only. Create a segment with no audio and add it to the rest.
            clip = VideoFileClip(videofile, audio = False).subclip(prevTime,nextTime)
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
            #v = VideoFileClip(videofile)

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
            clip = v.subclip(prevTime,nextTime)
            clips = concatenate([clips,clip])

            # Advance to next segment time.
            prevTime = nextTime


    videoLength = duration
    if prevTime > duration:
        prevTime = duration

    if ffmpeg_params != None:
        fparams = []
        for x in ffmpeg_params.split(' '):
            fparams.extend(x.split('='))
    else:
        fparams = None

    clip = v.subclip(prevTime,videoLength)
    print("created ending clip from " + str(prevTime) + " to " + str(videoLength))
    clips = concatenate([clips,clip])
    clips.write_videofile(outfile, codec=vcodec, fps=24, bitrate=videoBitrate, audio_bitrate=audioBitrate, audio_codec=acodec, ffmpeg_params=fparams, threads=threadNum, preset=ffmpegPreset, write_logfile=writeLogfile)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="Original input video file.")
    parser.add_argument("edlfile", help="EDL file with edit definitions.")
    parser.add_argument("outfile", help="Edited video file path/name.")
    parser.add_argument("-t", "--threads", type=int, help="Number of CPU threads to use.")
    parser.add_argument("-p", "--preset", choices=["ultrafast", "superfast", "fast", "medium", "slow", "superslow"], help="FFMPEG preset to use for optimizing the compression. Defaults to 'medium'.")
    parser.add_argument("-vb", "--videobitrate", help="Video bitrate setting. Auto-detected from original video unless specified.")
    parser.add_argument("-ab", "--audiobitrate", help="Audio bitrate setting. Auto-detected from original video unless specified.")
    parser.add_argument("-vc", "--vcodec", help="Video codec to use.")
    parser.add_argument("-ac", "--acodec", help="Audio codec to use.")
    parser.add_argument("-fp", "--ffmpegparams", help="Additional FFMpeg parameters to use. Example: '-crf=24 -s=640x480'.")
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

    mi = MediaInfo.parse(args.infile)
    if args.videobitrate == None:
        videoBitrate = str(int(mi.tracks[1].bit_rate / 1000)) + "k"
        print("Using original video bitrate: "+videoBitrate)
    else:
        videoBitrate = args.videobitrate
        if videoBitrate[-1] != 'k':
            videoBitrate = videoBitrate+'k'

    if args.audiobitrate == None:
        try:
            audioBitrate = str(int(mi.tracks[2].bit_rate / 1000)) + "k"
        except TypeError:
            audioBitrate = str(int(int(mi.tracks[2].bit_rate.split(' / ')[1]) / 1000)) + "k"

        print("Using original audio bitrate: "+audioBitrate)
    else:
        audioBitrate = args.audiobitrate
        if audioBitrate[-1] != 'k':
            audioBitrate = audioBitrate+'k'

    render(args.infile, estruct, args.outfile, videoBitrate, audioBitrate, threadNum=threadNum, vcodec=args.vcodec, acodec=args.acodec, ffmpeg_params=args.ffmpegparams, ffmpegPreset=ffmpegPreset)


if __name__ == "__main__":
    main()
    
