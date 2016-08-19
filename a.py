#!/usr/bin/python

from pygame import mixer

def play():
    mixer.init()
    mixer.music.load("test.mp3")
    mixer.music.play()

play()
