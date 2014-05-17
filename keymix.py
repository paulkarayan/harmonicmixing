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
import csv

capdir = os.getcwd()
directory = os.path.join(capdir, "songs")

echonestkey = os.environ.get('ECHO_NEST_API_KEY')
config.ECHO_NEST_API_KEY=echonestkey

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
log = Logger('Logbook')

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

def pickasong(shimsongdict, songname=None):
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


def findkeymatches(harmonic_mixing_dict, current_song_keysig):
    log.info("the current song's keysig, {0}, matched with these keysigs: {1} ",
             current_song_keysig, harmonic_mixing_dict[current_song_keysig])
    return harmonic_mixing_dict[current_song_keysig]



def findsongmatches(shimsongdict, current_song_matches):
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
    allsongdict = {}
    shimsongdict = {}

#get persisted songs and their metadata
    with open('test_songstore.csv', 'rb') as f:
      reader = csv.reader(f,)
      shimsongdict = dict((rows[0],int(rows[1])) for rows in reader)

    with open('test_songstore.csv', 'a+b') as f:  # Just use 'w' mode in 3.x
      w = csv.writer(f)

      ff = os.listdir(directory)
      for f in ff:
          if f.rsplit('.', 1)[1].lower() in ['mp3', 'aif', 'aiff', 'aifc', 'wav']:
                filename = os.path.join(directory, f)

                if filename in shimsongdict.keys():
                    log.info("the song that we didn't call api for: {0} ", filename)
 
                else:
                    filekey = audio.LocalAudioFile(filename, defer=True)
                    allsongdict[filename] = [keysig(filekey), mode(filekey),timesig(filekey), tempo(filekey)]

#sort of a shim thing to produce the format expected
                    shimsongdict[filename] = int(str(keysig(filekey)) + str(mode(filekey)))
                    log.info("the song that just was analyzed had a keysig of: {0} ", int(str(keysig(filekey)) + str(mode(filekey))))
                    w.writerow([filename, int(str(keysig(filekey)) + str(mode(filekey)))])

    log.debug("shimsongdict: {0},{1}", shimsongdict, type(shimsongdict))
    return shimsongdict

def harmonicmix(songname=None):

#note that you need to change this for Linux...
    outputstring = ("python " + capdir+ "\capsule\capsule.py -t 4 -i 60 -e ")
    shimsongdict = gatherfiles(directory)
    songnamelist = []
    while 1:
        
        songnamelist.append(songname)
#pass in songname if you want to seed it, otherwise it's a rand
        outputstring += ' "' + songname + '"'
        current_song_keysig = pickasong(shimsongdict, songname)
        current_song_matches = findkeymatches(harmonic_mixing_dict, current_song_keysig)
        songname = findsongmatches(shimsongdict, current_song_matches)

        
        
        if songname == "killswitch":
            break

        outputstring += ' "' + songname + '"'

    return outputstring, songnamelist

def mixmaster(iterations=100):
    counter = 0 
    while counter < iterations:
        
        pass

def mixgen(outputstring):
    log.info("calling subprocess to create combined mix")
    process = subprocess.Popen(outputstring, stdout=subprocess.PIPE, shell=True)
    stdoutdata, stderrdata = process.communicate()

    

#simple test - seed the ix w/ Dre Day
outputstring, songnamelist = harmonicmix(directory + '\Dr. Dre - Dre Day.mp3')
print(outputstring, songnamelist)
