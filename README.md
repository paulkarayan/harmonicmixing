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

this is a major wip. so it doesn't do any of this right now :)

current gaps:

- move API keys and directory locations to a Config file (vs. in code)

- clean out old comments

- move these to-dos to the issue tracker in Github

- change the output file name to something better than capsule.py

- improve on the output
   - cycle back through to try another mix if you only get 1-2 songs
   - figure out how to match so we get the longest possible mix (that's still delightful) from the songs in the directory
   - tempo or beat matching (see: http://www.surina.net/soundtouch/)
   - only link files that have a certain mood together. for example, don't mix metal and rap.

- write a nice narrative for the user about why the songs were linked together (or not... maybethis is a log)

- integrate with capsule.py
   - may need to modify the module to:
      - include the api key you're using in a config
      - figure out how long to make each song, default right now is 8 sec. could be random or a % of the total length, or random between 2-3 min (those that dont match will not be included... need to deal with this so we dont get gaps or bad mixes)
   - leverage the -t option to do tempo sorting. probably in concert with a much larger mix and constraints

- finish converting the prints to logbook for clarity
   - logbook needs to be controlled
   - clean out old logging

- make mocking easier so development is faster
   - use shimsongdict_mock 
   - use a copy of the dict if there's one available... or check to see if it's been updated, otherwise use cached dict 

- bug: keysigs of 0 and 1. wtf?
{'C:\\Users\\paulkarayan\\Documents\\GitHub\\harmonicmixing\\songs\\Dr. Dre - Dre Day.mp3': 71, 'C:\\Users\\paulkarayan\\Documents\\GitHub\\harmonicmixing\\songs\\Dr. Dre feat. Eminem - Forgot About Dre.mp3': 81, 'C:\\Users\\paulkarayan\\Documents\\GitHub\\harmonicmixing\\songs\\L\xfanasa - The Minor Bee.mp3': 110, 'C:\\Users\\paulkarayan\\Documents\\GitHub\\harmonicmixing\\songs\\dune bassoon 03162014_8.mp3': 70, 'C:\\Users\\paulkarayan\\Documents\\GitHub\\harmonicmixing\\songs\\Dr.Dre & Snoop Dogg- Still Dre.mp3': 51, 'C:\\Users\\paulkarayan\\Documents\\GitHub\\harmonicmixing\\songs\\Joyce Sims - (You Are My) All And All.mp3': 31, 'C:\\Users\\paulkarayan\\Documents\\GitHub\\harmonicmixing\\songs\\Hiiragi_Fukuda-Open_Fields_Blues.mp3': 21, 'C:\\Users\\paulkarayan\\Documents\\GitHub\\harmonicmixing\\songs\\Polish Girl - NEON INDIAN.mp3': 1},<type 'dict'>

- unit / integration tests
   - harmonicmix integration test
   - harmonicmix test that we get variety, and it's not including wrong songs
   - pickasong
   - findkeymatches
   - findsongmatches
   - gatherfiles
   - capsule integration test


- normalize the file structure
   - don't use an absolute directory
   - allow songs to be located somewhere else (parameterize? config?)


- allow user to limit number of songs we attempt to use. esp. important if we're going to scan them all... or perhaps you go until you hit an api rate limit?

- upload a completed mix to Soundcloud 

- logging added to subprocess entry / exit, upload etc... right now you just wait
