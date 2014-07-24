EDL Kit
=======

Dependencies: A recent [ffmpeg](http://www.ffmpeg.org/download.html), the [MoviePy](https://github.com/Zulko/moviepy) Python module, and VLC (for edltweak).

Tools:

edledit:
This script takes in as arguments:
* A video file.
* An EDL file.
* A file name to save the edited file to.

Example command: `python edledit.py "My Video.mp4" "My Video.edl" "My Video edited.mp4"`

The edits listed in the EDL file will be used to create an edited version of the original video.
See [here](http://www.mplayerhq.hu/DOCS/HTML/en/edl.html) for instructions on making an EDL file.

Currently, this script supports actions 1 and 0 (Mute, and Cut Video).


edltweak:
This script takes in as arguments:
* A video file.
* An EDL file.

Example command: `python edltweak.py "My Video.mp4" "My Video.edl"`

The script will start up a small curses-based UI that assists with making adjustments to (tweaking)
the timings in EDL files. It also hooks into VLC to show a rendering of the adjusted segment of the video.
The keyboard commands to operate the tool are all listed in the UI when it starts.
