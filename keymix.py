from pyechonest import config

config.ECHO_NEST_API_KEY=""

import sys, os
import echonest.remix.audio as audio
from pprint import pprint
from pyechonest import config


usage = """
Usage:
python keymix.py <inputDirectory> <outputFilename>

Example:
python keymix.py /path/to/mp3s djideas.txt
"""

import unittest
import random


#fake tests
#make 5 representations of songs
#then ensure that functions do what they should


#generate mock song representations. this will go into "setUp"

allsongdict = {"Arcade":111,"mock orange":121, "angrytime":120, "darkpup":121,
                   "oddoneout":60}


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



def pickasong(songname):
    return allsongdict.pop(songname)
     

def findkeymatches(current_song_keysig):
    return harmonic_mixing_dict[current_song_keysig]



def findsongmatches(current_song_matches):
    outputlist = []
    for keysig in current_song_matches:
        for name, value in allsongdict.items():
            if keysig == value:
                #print(name, value)
                outputlist.append(name)

    if outputlist.__len__() == 0:
        print("no more songs that match, you're done.")
        return "killswitch"

    print("enumrate output list:", *outputlist, sep=',')
    songname = random.choice(outputlist)
            
    return songname


def keysig(audiofile):
    return int(audiofile.analysis.key['value'])

def timesig(audiofile):
    return int(audiofile.analysis.time_signature['value'])

def mode(audiofile):
    return int(audiofile.analysis.mode['value'])

def gatherfiles(directory):
#returns a dict mocked by allsongdict
    
    ff = os.listdir(directory)
    for f in ff:
        # collect the audio files
        if f.rsplit('.', 1)[1].lower() in ['mp3', 'aif', 'aiff', 'aifc', 'wav']:
            # the new defer kwarg doesn't load the audio until needed
            filename = os.path.join(directory, f)
            
            filekey = audio.LocalAudioFile(filename, defer=True)
           
            keydict[filename] = (keysig(filekey), mode(filekey),timesig(filekey))
        # mind the rate limit
            print(keydict.items())

    print >> sys.stderr, 'making recommendations.',
    for song in aud:
        print >> sys.stderr, '.',

    f = open(outfile.txt, 'w')
    print("\n\nsong name, key, mode, and time signature \n")
    pprint(keydict)
    f.close()




def harmonicmix():
    #call gatherfiles, i fake it using allsongdict
    #seed it or ask for a random song. againt, i fake it.
    seed = "Arcade"
    print(seed)
    songname = seed
    

    while 1:
        current_song_keysig = pickasong(songname)
        #print(current_song_keysig, "current_song_keysig")
        current_song_matches = findkeymatches(current_song_keysig)
        #print(current_song_matches, "current_song_matches")
        songname = findsongmatches(current_song_matches)

        if songname == "killswitch":
            break
        
        print(songname, "<-- is the next song you'll hear")
        
    
#test 1
#harmonicmix()

#test that we get variety
##for x in range(0,10):
##    print(x, "\n")
##    harmonicmix()
##    allsongdict = {"Arcade":111,"mock orange":121, "angrytime":120, "darkpup":121,
##                   "oddoneout":60}



