import nltk
import speech_to_text
import text_to_speech

# text = nltk.word_tokenize("are their people .in the room ?")
# tags =  nltk.pos_tag(text)
#
# words =  [word for word, tag in tags if tag in ('NN','NNP','NNS')]
# print words
#
# text_to_speech(words)

#vision
text_to_speech.get_speech("command")
answer = speech_to_text.stt()
print answer
if answer.lower()=="vision":
    text_to_speech.get_speech("command")



#
# def enquire(words):
#     if len(words)>1:
#
#
