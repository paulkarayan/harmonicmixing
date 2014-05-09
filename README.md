harmonicmixing
==============

uses the concept of "harmonic mixing" (google it!) to create a delightful mix from your music collection.

to do so, the program discerns the keys (and bpm) of audio files in a directory using the echnoest API, and then links songs that will sound good together.

Instructions:
- clone this repo
- install the Echo Nest API key per the directions on Remix
   -(if you're using linux, you probably need to test Capsule.py because ffmpeg is flaky.) 
- add your Echo Nest API key to the script
- add your files to the Songs directory, or update the directory locations in the script
- run:
> python harmonicmix.py
- commit to this project since it could be dope

this is a major wip. it works end to end but leaves a lot to be desired :)
