from gtts import gTTS
import subprocess

def get_speech(sentence):
    tts = gTTS(text=sentence, lang='en')
    tts.save("test1.mp3")
    subprocess.Popen(['mpg123', '-q', "test1.mp3"]).wait()
