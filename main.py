import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import ollama


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        # Listen to the user's voice
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='PT-BR')
        print(f'User said: {query}')

        if query == 'fechar':
            print('finishing...')
            exit()
        # Pass the recognized query to respond()
        respond(query)

    except sr.UnknownValueError:
        print('Could not understand, please say that again...')
        listen()

    except sr.RequestError as e:
        print(f'Error with Google Speech Recognition service: {e}')

def respond(query):
    print('Responding...')
    response = ollama.chat(model='llama2', messages=[
    {
        'role': 'user',
        'content': query,
    },
    ])
    # Print the response message content
    res = response['message']['content']
    print(res)

    tts = gTTS(text=res, lang='en', slow=False)
    tts.save("pcvoice.mp3")
    # to start the file from python
    os.system("start pcvoice.mp3")

    # Continue listening after responding
    listen()

# Start the process by calling the listen function
listen()
