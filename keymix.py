from pyechonest import config
import logging
import subprocess
from logbook import Logger
import soundcloud


#config.ECHO_NEST_API_KEY=""

import sys, os
import echonest.remix.audio as audio
from pprint import pprint
from pyechonest import config
import unittest
import random

##usage = """
##Usage:
##python keymix.py <inputDirectory> <outputFilename>
##
##Example:
##python keymix.py /path/to/mp3s djideas.txt
##"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

log = Logger('Logbook')


# PC directory ... just uncomment to test
directory = "C:\Users\paulkarayan\Documents\GitHub\harmonicmixing\songs"
capdir = "C:\Users\paulkarayan\Documents\GitHub\harmonicmixing"

#Linux directory -for songs
#directory = "/home/paulkarayan/harmonicmixing/songs/"

#linux directory for the capsule script
#capdir = "/home/paulkarayan/harmonicmixing/"

shimsongdict_mock = {"Arcade":111,"mock orange":121, "angrytime":120, "darkpup":121,
                   "oddoneout":60}


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

    #print("enumerate output list:", *outputlist, sep=',')
    #stupid old python versions wont work w ^^
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


def gatherfiles(directory):
#returns a dict mocked by shimsongdict_mock

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
    log.debug("shimsongdict_mock: {0},{1}", shimsongdict_mock, type(shimsongdict_mock))
    return shimsongdict

def harmonicmix(songname=None):
#call gatherfiles, i fake it using allsongdict
# by commenting out below and setting shimsongdict = shimsongdict_mock

#seed it or ask for a random song. againt, i fake it.
##    seed = "Arcade"
##    print(seed)
##    songname = seed

#note that you need to change this for Linux...
    outputstring = ("python " + capdir+ "\capsule\capsule.py -t 4 -i 20 -e ")
    shimsongdict = gatherfiles(directory)
    #shimsongdict = shimsongdict_mock


    while 1:

#pass in songname if you want to seed it
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

#basic tests

#test that we get variety
##for x in range(0,2):
##    print(x, "\n")
##    harmonicmix(directory + '\Dr. Dre - Dre Day.mp3')
##

#auth for soundcloud...

# create a client object with access token
##client = soundcloud.Client(access_token='')

harmonicmix(directory + '\Dr. Dre - Dre Day.mp3')

### upload audio file
##track = client.post('/tracks', track={
##    'title': 'Harmonic Mixify - a mix for you',
##    'asset_data': open('capsule.mp3', 'rb')
##})
##
### print track link
##print(track.permalink_url)

#tests
##harmonicmix integration test
##harmonicmix test that we get variety, and it's not including wrong songs
##pickasong
##findkeymatches
##findsongmatches
