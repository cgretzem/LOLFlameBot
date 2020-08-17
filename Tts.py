from gtts import gTTS

import os




def getSpeech(textS):
    wd = os.getcwd()
    lan = 'en-uk'
    speech = gTTS(text = textS, lang = lan, slow = False)
    name = textS.replace(' ', '').replace('.', '').replace(',', '').replace('?', '').replace('!', '').replace("'", '')
    
    path = '{}/Speech/{}.mp3'.format(wd, name)
    print(path)
    try:
        speech.save(path)
    except FileNotFoundError:
        os.mkdir('Speech')
        print('Making dir')
        speech.save(path)
    return path

def delSpeech(path):
    os.remove(path)



def main():
    exampleText = 'Hullo, this is a test'
    lang = 'en-tz'
    speech = gTTS(text = exampleText, lang = lang, slow = False)
    path = './Speech/bonk.mp3'
    try:
        speech.save(path)
    except FileNotFoundError:
        os.mkdir('Speech')
        speech.save(path)

if __name__ == '__main__':
    main()