#!/usr/bin/python

# from pygame import mixer
#
#
# mixer.init()
# mixer.music.load("test.mp3")
# mixer.music.play()

import subprocess

def play_mp3():
    subprocess.Popen(['mpg123', '-q', "test.mp3"]).wait()

play_mp3()
