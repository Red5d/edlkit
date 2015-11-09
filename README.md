EDL Kit
=======

Dependencies: A recent [ffmpeg](http://www.ffmpeg.org/download.html), the [MoviePy](https://github.com/Zulko/moviepy) Python module, and VLC (for edltweak and the edlcreate scripts).

I'm developing this on Linux, but working on full Windows support in the future. Currently, if you have ffmpeg and the MoviePy Python module set up on Windows, the edledit script works.

##edledit

This script takes in as arguments:
* A video file.
* An EDL file.
* A file name to save the edited file to.

Available options are:
* -t, Number of process threads to use: A number from 0 to the number of CPU cores you have. Defaults to 2 if not specified.
* -p, ffmpeg preset to use: Adjusts speed and efficiency of the compression. Defaults to "medium" if not specified.
* -b, Video bitrate: Automatically detected from original if not specified. Defaults to "2000k" if not specified and auto-detection fails.

Usage info is available using the "-h" option.

Example command: `python3 edledit.py "Video.mp4" "Video.edl" "Video-edited.mp4" -t 3`

The edits listed in the EDL file will be used to create an edited version of the original video.
See [here](http://www.mplayerhq.hu/DOCS/HTML/en/edl.html) for instructions on making an EDL file.

Currently, this script supports actions 1 and 0 (Mute, and Cut Video).


##edltweak

This script takes in as arguments:
* A video file.
* An EDL file.

Example command: `python edltweak.py "My Video.mp4" "My Video.edl"`

The script will start up a small text-based UI that assists with making adjustments to (tweaking)
the timings in EDL files. It also hooks into VLC to show a rendering of the adjusted segment of the video.
The keyboard commands to operate the tool are all listed in the UI when it starts.


##edltweak-gui

This script does the same thing as edltweak, but it has a Python 3 TTK (Tkinter) GUI instead of the text-based UI.

The same arguments as edltweak work, but it also has a file-selection dialog you can use if you run it without arguments.


##edlcreate

This script takes in as arguments:
* A video file.
* An EDL filename (to output to).

Example command: `python edlcreate.py "My Video.mp4" "My Video.edl"`

A curses-based UI and VLC start up and let you mark edit times in the video as you watch. Marked times will
be written to the EDL file you specified. The keyboard commands are all listed in the UI when it starts.


##edlcreate-timer

This script takes in as arguments:
* An EDL filename (to output to).

Example command: `python edlcreate.py "My Video.edl"`

This one works exactly the same as the edlcreate script, but uses a timer to determine the time when you mark
an edit instead of reading from VLC. This is useful if you want to mark edits while watching a live TV show 
that you're recording or going to acquire the video file for it later.
