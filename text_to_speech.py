from gtts import gTTS


tts = gTTS(text='Hello chill bro !', lang='en')
tts.save("test.mp3")


from pygame import mixer

def play():
    mixer.init()
    mixer.music.load("test.mp3")
    mixer.music.play()

play()
