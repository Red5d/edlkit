from setuptools import setup, find_packages
setup(
    name = "EDLKit",
    version = "1.0",
    description = "Python tools to create, tweak, and apply EDL file edits to video files.",
    url = "https://github.com/Red5d/edlkit",
    author = "Red5d",
    license = "GPLv2",
    keywords = "video edl ffmpeg moviepy edit editing",
    
    packages = find_packages(),
    install_requires = ['moviepy>=0.2.2'],
    scripts = ['edledit.py', 'edlcreate.py', 'edlcreate_timer.py', 'edltweak_gui.py'],
    entry_points={
        'console_scripts': [
            'edledit = edledit:main',
            'edlcreate = edlcreate',
            'edlcreate_timer = edlcreate_timer',
        ],
        'gui_scripts': [
            'edltweak_gui = edltweak_gui',
        ]
    }
)

