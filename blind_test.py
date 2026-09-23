import multiprocessing
from os import remove, listdir as ls
from os.path import isfile
from sys import argv, exit
from multiprocessing import Process, Condition
from time import time_ns as ns, sleep
from pydub import AudioSegment
from pydub.playback import play
#import PySide6


class Player(object):
    def __init__(self, audio_obj, file_name):
        self.audio = audio_obj
        self.id = file_name
        self.started, self.timestamp = False, False
        self.timer = 0
    
    def play(self, timestamp=''):
        self.started = True
        if timestamp:
            self.to_play = self.audio self.timestamp = True
        else:
            self.to_play = self.audio
        self.proc = Process(target=play, args=(self.to_play, ))
        self.proc.start()
        self.timer = ns()

    def stop(self):
        self.timer = ns() - self.timer
        self.proc.terminate()
        self.started, self.timestamp = False, False
        return self.timer

    def get_timestamp(self):
        return ns() - self.timer if self.started else None

    def get_id(self):
        return self.id


def prep(org, name):
    fname = lambda n, fmt, bitrate: n + '_' + bitrate + '.' + fmt
    bitrates = '1411k 320k 128k'.split()
    for b in bitrates:
        wav, mp3 = fname(name, 'wav', b), fname(name, 'mp3', b)
        print(f'Generating {wav}')
        if b == '1411k':
            org.export(wav, format='wav')
            continue
        org.export(mp3, format='mp3', bitrate=b)
        AudioSegment.from_mp3(mp3).export(wav, format='wav')
        remove(mp3)
    fnames = return {f: AudioSegment.from_file(f) for f in fnames}


def main():
    if len(argv) != 2:
        exit('Usage: python blind-test.py file_name_wo_extensions')
    n = argv[1]
    t = n + '_1411k.wav'
    src = t if t in ls() else [0]
    if not isfile(src):
        exit(f'File {argv[1]} not found')
    
    audios = prep(AudioSegment.from_file(src), n)
    players = record_time = 0
    for _ in range(20):
        players[0].play(record_time)
        sleep(1)
        record_time += players[0 1].play(record_time)
        sleep(1)
        record_time += players[1].stop() // 1_000_000


if __name__ == '__main__':
    main()