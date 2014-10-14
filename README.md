EDL Kit
=======

Dependencies: A recent [ffmpeg](http://www.ffmpeg.org/download.html), the [MoviePy](https://github.com/Zulko/moviepy) Python module, and VLC (for edltweak and the edlcreate scripts).

I'm developing this on Linux, but working on full Windows support in the future. Currently, if you have ffmpeg and the MoviePy Python module set up on Windows, the edledit script works.

##edledit

This script takes in as arguments:
* A video file.
* An EDL file.
* A file name to save the edited file to.

Example command: `python edledit.py "My Video.mp4" "My Video.edl" "My Video edited.mp4"`

The edits listed in the EDL file will be used to create an edited version of the original video.
See [here](http://www.mplayerhq.hu/DOCS/HTML/en/edl.html) for instructions on making an EDL file.

Currently, this script supports actions 1 and 0 (Mute, and Cut Video).


##edltweak

This script takes in as arguments:
* A video file.
* An EDL file.

Example command: `python edltweak.py "My Video.mp4" "My Video.edl"`

The script will start up a small curses-based UI that assists with making adjustments to (tweaking)
the timings in EDL files. It also hooks into VLC to show a rendering of the adjusted segment of the video.
The keyboard commands to operate the tool are all listed in the UI when it starts.


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
