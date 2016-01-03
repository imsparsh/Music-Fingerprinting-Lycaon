Music Fingerprinting | Lycaon
=============================

Music Fingerprinting in python that not only recognizes the exact song but also the similar ones using Locality Sensitive Hashing.

**Technologies Used:**
-python # back end programming with GUI
-MongoDB # database

*This is a complete audio fingerprint project with GUI based on PyQT4, and MongoDB database.

- **fingerprint.py**
GUI module used for Fingerprinting the songs to build the database.

- **Lycaon.py**
GUI module for searching the songs through an audio file or using the microphone input (make sure the audio quality is good).

- **./albumart/**
directory that stores the albumart of the input songs.

- **./db_info/**
directory that has instructions for setting up the database.

- **./docs/**
directory that consists of Documents for the explanation of the program.

- **./fingerprint**
directory that acts as base for calculating the fingerprint of an audio file that is controlled through multiprocessing.

- **./icons**
directory that consists some icons for GUI

- **./metadata**
directory that consists the handling of metadata of the given songs for fingerprint.

- **./record**
directory that consists the recording module for real time audio scan for searching a song using microphone.

- **./sample**
directory that stores the temporary file in wave, captured using record module.

- **images_rc.pyc**
compiled python file that consists the images used in GUI.


Usage:
```
# make sure the database is ready and running..
# all the dependencies in requirements.txt are installed..
python fingerprint.py # select songs and fingerprint.
python Lycaon.py # provide audio and search your song.
```

* This program is build and configured on windows 8 platform, for others like linux, MacOS, it would need some changes in the modules used, help it yourself.
Good Luck.