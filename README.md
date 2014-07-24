edledit
=======

Dependencies: A recent [ffmpeg](http://www.ffmpeg.org/download.html), and the [MoviePy](https://github.com/Zulko/moviepy) Python module.

This script takes in as arguments:
* A video file.
* An EDL file.
* A file name to save the edited file to.

Example command: `python edledit.py "My Video.mp4" "My Video.edl" "My Video edited.mp4"`

The edits listed in the EDL file will be used to create an edited version of the original video.
See [here](http://www.mplayerhq.hu/DOCS/HTML/en/edl.html) for instructions on making an EDL file.

Currently, this script supports actions 1 and 0 (Mute, and Cut Video).
