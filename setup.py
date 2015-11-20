from setuptools import setup, find_packages
setup(
    name = "EDLKit",
    version = "1.0",
    packages = find_packages(),
    install_requires = ['moviepy>=0.2.2'],
    entry_points={
        'console_scripts': [
            'edledit = edledit',
            'edlcreate = edlcreate',
            'edlcreate_timer = edlcreate_timer',
        ],
        'gui_scripts': [
            'edltweak_gui = edltweak_gui',
        ]
    }
)

