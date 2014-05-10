from pyechonest import config
import logging
import subprocess
from logbook import Logger
import soundcloud
import sys
import os
import sys, os
import echonest.remix.audio as audio
from pprint import pprint
from pyechonest import config
import unittest
import random

capdir = os.getcwd()
directory = os.path.join(capdir, "songs")

echonestkey = os.environ.get('ECHO_NEST_API_KEY')
config.ECHO_NEST_API_KEY=echonestkey

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
log = Logger('Logbook')

allsongdict = {}
shimsongdict = {}

harmonic_mixing_dict = {11:[121,11,21,10],
21:[11,21,31,20],
31:[21,31,41,30],
41:[31,41,51,40],
51:[41,51,61,50],
61:[51,61,71,60],
71:[61,71,81,70],
81:[71,81,91,80],
91:[81,91,101,90],
101:[91,101,111,100],
111:[101,111,121,110],
121:[111,121,11,120],
10:[120,10,20,11],
20:[10,20,30,21],
30:[20,30,40,31],
40:[30,40,50,41],
50:[40,50,60,51],
60:[50,60,70,61],
70:[60,70,80,71],
80:[70,80,90,81],
90:[80,90,100,91],
100:[90,100,110,101],
110:[100,110,120,111],
120:[110,120,10,121]}

def pickasong(songname=None):
    log.info('picking a song from shimsongdict')
    if songname == None:
        key = random.choice(shimsongdict.keys())
        log.debug("key type: {0}", type(key))
        pickedsong = shimsongdict.pop(key)
        songname = key
    else:
        pickedsong = shimsongdict.pop(songname)


    log.info('picked song: {0} with keysig {1}', songname, pickedsong)
    return pickedsong


def findkeymatches(current_song_keysig):
    log.info("the current song's keysig, {0}, matched with these keysigs: {1} ",
             current_song_keysig, harmonic_mixing_dict[current_song_keysig])
    return harmonic_mixing_dict[current_song_keysig]



def findsongmatches(current_song_matches):
    outputlist = []
    for keysig in current_song_matches:
        for name, value in shimsongdict.items():
            if keysig == value:
                log.info("the song that got matched with: {0}{1} ", name,value)
                outputlist.append(name)

    if outputlist.__len__() == 0:
        log.info("no more songs that match, you're done.")
        return "killswitch"

    log.info("enumerate output list:")
    for x in outputlist:
        log.info(x)

    songname = random.choice(outputlist)

    return songname


def keysig(audiofile):
    return int(audiofile.analysis.key['value'])

def timesig(audiofile):
    return int(audiofile.analysis.time_signature['value'])

def mode(audiofile):
    return int(audiofile.analysis.mode['value'])

def tempo(audiofile):
    return int(audiofile.analysis.tempo['value'])


#returns a dict mocked by shimsongdict_mock
def gatherfiles(directory):

    ff = os.listdir(directory)
    for f in ff:
        if f.rsplit('.', 1)[1].lower() in ['mp3', 'aif', 'aiff', 'aifc', 'wav']:
            filename = os.path.join(directory, f)

            filekey = audio.LocalAudioFile(filename, defer=True)

            allsongdict[filename] = [keysig(filekey), mode(filekey),timesig(filekey), tempo(filekey)]

#sort of a shim thing to produce the format expected
            shimsongdict[filename] = int(str(keysig(filekey)) + str(mode(filekey)))
            log.info("the song that just was analyzed had a keysig of: {0} ", int(str(keysig(filekey)) + str(mode(filekey))))


    print >> sys.stderr, 'making recommendations.'

    f = open("outfile.txt", 'w')
    f.close()
    log.debug("shimsongdict: {0},{1}", shimsongdict, type(shimsongdict))
    return shimsongdict

def harmonicmix(songname=None):

#note that you need to change this for Linux...
    outputstring = ("python " + capdir+ "\capsule\capsule.py -t 4 -i 60 -e ")
    shimsongdict = gatherfiles(directory)
    #shimsongdict = shimsongdict_mock


    while 1:

#pass in songname if you want to seed it, otherwise it's a rand
        outputstring += ' "' + songname + '"'
        print(outputstring)
        current_song_keysig = pickasong(songname)
        #print(current_song_keysig, "current_song_keysig")
        current_song_matches = findkeymatches(current_song_keysig)
        #print(current_song_matches, "current_song_matches")
        songname = findsongmatches(current_song_matches)

        if songname == "killswitch":
            break

        print(songname, "<-- is the next song you'll hear")
        outputstring += ' "' + songname + '"'
        print(outputstring)

    process = subprocess.Popen(outputstring, stdout=subprocess.PIPE, shell=True)
    stdoutdata, stderrdata = process.communicate()
    print(process.returncode, "return code")

    return outputstring


#simple test - seed the ix w/ Dre Day
harmonicmix(directory + '\Dr. Dre - Dre Day.mp3')
