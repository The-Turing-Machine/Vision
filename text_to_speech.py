from gtts import gTTS
import subprocess

def get_speech(sentence):
    tts = gTTS(text="command", lang='en')
    tts.save("test.mp3")
    subprocess.Popen(['mpg123', '-q', "test.mp3"]).wait()
