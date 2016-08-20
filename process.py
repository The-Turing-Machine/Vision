import nltk
import speech_to_text
import text_to_speech

def noun(answer):

    if "everything" in answer.lower():
        pass
    text = nltk.word_tokenize(answer)
    tags =  nltk.pos_tag(text)

    words =  [word for word, tag in tags if tag in ('NN','NNP','NNS')]
    print words


    if len(words)==1:
        text_to_speech.get_speech("Are you looking for"+ words[0])
        answer = speech_to_text.stt()
        print answer
        if "yes" in answer.lower() or "ya" in answer.lower() or "yup" in answer.lower():
            pass
    elif(len(words)>1):

        for i in range(len(words)):
            a = words[i]+" or"
        print a
        a = a[:-2]
        print a
        text_to_speech.get_speech("What are you looking for"+ a)
        answer = speech_to_text.stt()
        for i in len(words):
            if words[i] in answer.lower():
                pass




#vision


while(True):
    text_to_speech.get_speech("command")
    answer = speech_to_text.stt()
    print answer
    if "vision" in answer.lower():
        text_to_speech.get_speech("How may i help you ?")
        answer = speech_to_text.stt()
        noun(answer)
    else:
        text_to_speech.get_speech("Oops! Didn't catch that,pardon!")
