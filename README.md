harmonicmixing
==============

uses the concept of "harmonic mixing" (link:____) to create a delightful mix (and upload it to soundcloud) from your music collection.

to do so, it discerns the keys (and bpm) of audio files in a directory using the echnoest API.

this is a major wip. so it doesn't do any of this right now :)

current gaps:

- fake integration (e.g. return songs in format that can be typed into capsule on command line)

- figure out the looping bug (e.g. I don't feed the selected song back into the top)

- write a nice narrative for the user about why the songs were linked together (or not... maybethis is a log)

- integrate with capsule.py
-- may want to just link songs together for now
-- need to deal with inability to have spaces (unless in "") and hatred for periods...
-- may need to modify the module to:
--- include the api key you're using somehow passed in or in a config
--- figure out how long to make each song, default right now is 8 sec. could be random or a % of the total length, or random between 2-3 min (those that dont match will not be included... need to deal with this so we dont get gaps or bad mixes)

- finish converting the prints to logbook for clarity
-- logbook needs to be controlled
-- clean out old logging

- make mocking easier so development is faster
-- use shimsongdict_mock 
-- use a copy of the dict if there's one available... or check to see if it's been updated, otherwise use cached dict 

- bug: keysigs of 0 and 1. wtf?
{'C:\\Users\\paulkarayan\\Documents\\GitHub\\harmonicmixing\\songs\\Dr. Dre - Dre Day.mp3': 71, 'C:\\Users\\paulkarayan\\Documents\\GitHub\\harmonicmixing\\songs\\Dr. Dre feat. Eminem - Forgot About Dre.mp3': 81, 'C:\\Users\\paulkarayan\\Documents\\GitHub\\harmonicmixing\\songs\\L\xfanasa - The Minor Bee.mp3': 110, 'C:\\Users\\paulkarayan\\Documents\\GitHub\\harmonicmixing\\songs\\dune bassoon 03162014_8.mp3': 70, 'C:\\Users\\paulkarayan\\Documents\\GitHub\\harmonicmixing\\songs\\Dr.Dre & Snoop Dogg- Still Dre.mp3': 51, 'C:\\Users\\paulkarayan\\Documents\\GitHub\\harmonicmixing\\songs\\Joyce Sims - (You Are My) All And All.mp3': 31, 'C:\\Users\\paulkarayan\\Documents\\GitHub\\harmonicmixing\\songs\\Hiiragi_Fukuda-Open_Fields_Blues.mp3': 21, 'C:\\Users\\paulkarayan\\Documents\\GitHub\\harmonicmixing\\songs\\Polish Girl - NEON INDIAN.mp3': 1},<type 'dict'>

- unit / integration tests
-- harmonicmix integration test
--harmonicmix test that we get variety, and it's not including wrong songs
--pickasong
--findkeymatches
--findsongmatches
--gatherfiles
--capsule integration test

- improve on the output
-- cycle back through to try another mix if you only get 1-2 songs
-- figure out how to match so we get the longest possible mix (that's still delightful) from the songs in the directory. 