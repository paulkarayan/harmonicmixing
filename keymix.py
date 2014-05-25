from pyechonest import config
import logging
import subprocess
from logbook import Logger, FileHandler, SyslogHandler, NullHandler
import soundcloud
import sys
import os
import sys
import echonest.remix.audio as audio
from pprint import pprint
from pyechonest import config
import unittest
import random
import csv
import itertools
from collections import defaultdict
import glob

capdir = os.getcwd()
directory = os.path.join(capdir, "songs")

echonestkey = os.environ.get('ECHO_NEST_API_KEY')
config.ECHO_NEST_API_KEY=echonestkey

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
log = Logger('Logbook')
file_handler = FileHandler("keymixlog.log")
#error_handler = SyslogHandler('logbook example', level='ERROR')

#this seems to work though :)
null_handler = NullHandler()

harmonic_mixing_dict = {80:[10,80,30,101],
30:[80,30,110,61],
110:[30,110,50,11],
50:[110,50,0,81],
0:[50,0,70,31],
70:[0,70,20,91],
20:[70,20,90,51],
90:[20,90,40,1],
40:[90,40,100,71],
100:[40,100,60,21],
60:[100,60,10,111],
10:[60,10,80,41],

101:[41,101,61,80],
61:[101,61,11,30],
11:[61,11,81,110],
81:[11,81,31,50],
31:[81,31,91,0],
91:[31,91,51,70],
51:[91,51,1,20],
1:[51,1,71,90],
71:[1,71,21,40],
21:[71,21,111,100],
111:[21,111,41,60],
41:[111,41,101,10]
}

def pickasong(shimsongdict, songname=None):
    log.debug('picking a song from shimsongdict')

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
    log.debug("the current song's keysig, {0}, matched with these keysigs: {1} ",
             current_song_keysig, harmonic_mixing_dict[current_song_keysig])
    return harmonic_mixing_dict[current_song_keysig]



def findsongmatches(shimsongdict, current_song_matches):
    outputlist = []
    
    for keysig in current_song_matches:
        for name, value in shimsongdict.items():
        
            if keysig == value:
                log.debug("the song that got matched with: {0}{1} ", name,value)
                outputlist.append(name)

    if outputlist.__len__() == 0:
        log.info("no more songs that match, you're done.")
        return "killswitch"

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
                    log.debug("the song that we didn't call api for: {0} ", filename)
        
                else:
                    filekey = audio.LocalAudioFile(filename, defer=True)
                    allsongdict[filename] = [keysig(filekey), mode(filekey),timesig(filekey), tempo(filekey)]

                    log.debug(str(keysig(filekey)) + str(mode(filekey)),len(str(keysig(filekey)) + str(mode(filekey))),"<--len of keysig")
                    if len(str(keysig(filekey)) + str(mode(filekey))) < 2:
                        log.debug("skipped a keysig of {0}", keysig)
                    else:
#sort of a shim thing to produce the format expected
                        shimsongdict[filename] = int(str(keysig(filekey)) + str(mode(filekey)))
                        log.debug("the song that just was analyzed had a keysig of: {0} ", int(str(keysig(filekey)) + str(mode(filekey))))
                        w.writerow([filename, int(str(keysig(filekey)) + str(mode(filekey)))])

    log.debug("shimsongdict: {0},{1}", shimsongdict, type(shimsongdict))
    return shimsongdict

def harmonicmix(shimsongdict, songname=None):

#note that you need to change this for Linux...
    outputstring = ("python " + capdir+ "\capsule\capsule.py -t 4 -i 30 -e -s ")
    songnamelist = []
    while 1:
        

        
        current_song_keysig = pickasong(shimsongdict, songname)
        current_song_matches = findkeymatches(harmonic_mixing_dict, current_song_keysig)
        songname = findsongmatches(shimsongdict, current_song_matches)

        
        
        if songname == "killswitch":
            break

#capsule.py seems to fail with too many songs, so for the time being, restrict to 10

        if len(songnamelist) > 10:
            break
        
        songnamelist.append(songname)
        outputstring += ' "' + songname + '"'

    return outputstring, songnamelist

def mixmaster(iterations=5):
    
    topgoodness = 0
    topos = ""
    goodnessdict = extenddict()
    counter = 0 
    
    
    shimsongdict = gatherfiles(directory)
    rlist = list(shimsongdict.keys())
   
    for lt in (itertools.repeat(rlist)):
        shimsongdict = gatherfiles(directory)
        song = random.choice(lt)
        
        outputstring, songnamelist = harmonicmix(shimsongdict, song)
 
        shimsongdict = gatherfiles(directory)
        goodness = goodnessgracious(outputstring, songnamelist)
        counter += 1
        goodnessdict[outputstring] = goodness
        if counter > iterations:
            break
        

    for ose, mixgoodness in goodnessdict.items():
    #    print(ose, mixgoodness, type(ose), type(mixgoodness),"<-----")
        for m in mixgoodness:
            if m > topgoodness:
                topgoodness = m
                topos = ose

    
    log.info("the best goodness score was {0}, from song {1}", topgoodness, topos)

    mixgen(topos)

    #assume that newest mp3 file is the one we just made

    newest = max(glob.iglob('*.[Mm][Pp]3'), key=os.path.getctime)

    return newest


    
def mixgen(outputstring):
    log.info("calling subprocess to create combined mix")
    print("calling subprocess to create combined mix")
    process = subprocess.Popen(outputstring, stdout=subprocess.PIPE, shell=True)
    stdoutdata, stderrdata = process.communicate()

def goodnessgracious(outputstring,songnamelist=None): 
#this is a measure of the mix's goodness. this could be
#a weighting of style stdev, bpm, repeated artists, etc..
#but for now it's just # of songs in the mix. and approx. by
#outputstring length (which should be roughly correct) so also
#ignoring the songnamelist for now but it'll be needed in future

    goodness = len(outputstring)

    return goodness 


def soundcloudupload(mixfilename='captemp.mp3'):
    client_id = os.environ.get('SOUNDCLOUD_CLIENT_ID')
    client_secret = os.environ.get('SOUNDCLOUD_CLIENT_SECRET')
    username = raw_input('Enter your SoundCloud username: ')
    password = raw_input('Enter your SoundCloud password: ')



    client = soundcloud.Client(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password
    )
    
    print("logged in successfully as: %", % client.get('/me').username)

    track = client.post('/tracks', track={
    'title': 'Harmonic Mix %s' % mixfilename,
    'sharing': 'private',
    'description': 'Someone should add the song names in the mix here',
    'asset_data': open(mixfilename, 'rb')
})

    print("uploaded your mix as: %s", track.title)



class extenddict(dict):

    def __setitem__(self, key, value):
        """add the given value to the list of values for this key"""
        self.setdefault(key, []).append(value)


 


with file_handler.threadbound():
    newest = mixmaster()
    soundcloudupload(newest)
    

