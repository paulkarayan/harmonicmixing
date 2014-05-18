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

this is a work in progress, but it works end-to-end pretty well. 

i would love another set of eyes on the core harmonic mixing implementation, as well as help with the beat matching and "goodness" function.

common issues:

- capsule.py is a bit flakey esp. with large numbers of songs, and my implementation doesn't provide much insight into how the process is progressing (or even if it's worked or not). i've restricted the upper limit of songs you can mix for now which helps with both problems.
- capsule.py and echonest in general needs ffmpeg, which sucks to get working on linux. thoughts here would be very useful!
