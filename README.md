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
* -vb, Video bitrate: Automatically detected from original if not specified.
* -ab, Audio bitrate: Automatically detected from original if not specified.

Usage info is available using the "-h" option.

Example command: `python3 edledit.py "Video.mp4" "Video.edl" "Video-edited.mp4" -t 3`

The edits listed in the EDL file will be used to create an edited version of the original video.
See [here](http://www.mplayerhq.hu/DOCS/HTML/en/edl.html) for instructions on making an EDL file.

Currently, this script supports actions 1, 0 (Mute, and Cut Video), and my custom action (2) which 
cuts out the selected audio and speeds up the video enough to cover the audio cut and resync the video.


##edltweak_gui

This script takes in as arguments:
* A video file.
* An EDL file.

The script can also be run without arguments and the files selected in the GUI.

Example command: `python edltweak_gui.py "My Video.mp4" "My Video.edl"`

The script will start up a Python3 TTK (Tkinter) GUI that assists with making adjustments to (tweaking)
the timings and edit types in EDL files. It also hooks into VLC to show a rendering of the adjusted segment of the video.
The keyboard commands to operate the tool can be viewed by clicking the "Keyboard Controls" button after starting it.

The functionality from the edlcreate script is now bundled into this as well. Pressing "o" (for Original) will
play the video file in vlc, and you can mark edit points to save to an EDL file with "m" just like edlcreate while
the original video is playing.


##edltweak

This script does mostly the same thing as edltweak, but it has a text-based curses UI.

Development has shifted to edltweak_gui now and this script will likely not be updated.


##edlcreate

This script takes in as arguments:
* A video file.
* An EDL filename (to output to).

Example command: `python edlcreate.py "My Video.mp4" "My Video.edl"`

A curses-based UI and VLC start up and let you mark edit times in the video as you watch. Marked times will
be written to the EDL file you specified. The keyboard commands are all listed in the UI when it starts.


##edlcreate_timer

This script takes in as arguments:
* An EDL filename (to output to).

Example command: `python edlcreate.py "My Video.edl"`

This one works exactly the same as the edlcreate script, but uses a timer to determine the time when you mark
an edit instead of reading from VLC. This is useful if you want to mark edits while watching a live TV show 
that you're recording or going to acquire the video file for it later.
