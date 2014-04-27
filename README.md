harmonicmixing
==============

uses the concept of "harmonic mixing" (link:____) to create a delightful mix (and upload it to soundcloud) from your music collection.

to do so, it discerns the keys (and bpm) of audio files in a directory using the echnoest API.

this is a major wip. so it doesn't do any of this right now :)

current gaps:
- get capsule.py to create longer songs (use the examples)

- get some real songs that would link together nicely and test with them

- write a nice log / narrative for the user about why the songs were linked together

- integrate with capsule.py
-- may want to just link songs together for now

- finish converting the prints to logbook for clarity
-- logbook needs to be controlled
-- clean out old logging

- make mocking easier so development is faster

- unit / integration tests
-- harmonicmix integration test
--harmonicmix test that we get variety, and it's not including wrong songs
--pickasong
--findkeymatches
--findsongmatches
--gatherfiles
--capsule integration test

