import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import ollama
import pyttsx3

engine = pyttsx3.init()
    
ollama.chat(model='llama3.2:1b', messages=[
    {
        'role': 'system',
        'content': '',
    },
    ])

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        # Listen to the user's voice
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-IN')
        print(f'User said: {query}')

        if query == 'bye':
            res = 'bye bye!'
            print(res)
            engine.say(res)
            engine.runAndWait()
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
    response = ollama.chat(model='llama3.2:1b', messages=[
    {
        'role': 'user',
        'content': query,
    },
    ])
    # Print the response message content
    res = response['message']['content']
    print(res)

    
    # Get available voices
    voices = engine.getProperty('voices')

    # Set voice by ID (adjust based on the desired gender or age)
    # Example: selecting a male voice (adjust based on available IDs)
    # Set a specific voice by its ID
    voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'  # Replace with the actual voice ID from the list
    engine.setProperty('voice', voice_id)


    # Optionally, set speech rate and volume
    engine.setProperty('rate', 200)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

    # Speak some text
    engine.say(res)
    engine.runAndWait()
    # Continue listening after responding
    listen()

# Start the process by calling the listen function
listen()
