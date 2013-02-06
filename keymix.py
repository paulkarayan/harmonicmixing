# cd c:\python27
# python keymix.py remix-master\examples\music\ djtest.txt


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


def main(directory, outfile):
    # pick up all the files in the directory
    # todo: need to make sure it'll get into subdirs
    aud = []
    keydict = {}
    ff = os.listdir(directory)
    for f in ff:
        # collect the audio files
        if f.rsplit('.', 1)[1].lower() in ['mp3', 'aif', 'aiff', 'aifc', 'wav']:
            # the new defer kwarg doesn't load the audio until needed
            filename = os.path.join(directory, f)
            #aud.append(audio.LocalAudioFile(filename, defer= True))
            filekey = audio.LocalAudioFile(filename, defer=True)
            
            keydict[filename] = (keysig(filekey), mode(filekey),timesig(filekey))
        # mind the rate limit
            print(keydict.items())
    #num_files = len(aud)

    #for entry in aud:
    #    print(entry, '<-- files')

    #print >> sys.stderr, "Sorting files by key..."

    # sort by key signature: 
    aud.sort(key=keysig)

    print >> sys.stderr, 'making recommendations.',
    for song in aud:
        print >> sys.stderr, '.',

    f = open(outfile, 'w')
    print("\n\nsong name, key, mode, and time signature \n")
    pprint(keydict)
    f.close()

def keysig(audiofile):
    return int(audiofile.analysis.key['value'])

def timesig(audiofile):
    return int(audiofile.analysis.time_signature['value'])

def mode(audiofile):
    return int(audiofile.analysis.mode['value'])



if __name__ == '__main__':
    try:
        directory = sys.argv[1]
        outfile = sys.argv[2]
        
    except:
        print usage
        sys.exit(-1)
    main(directory, outfile)
