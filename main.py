
import speech_recognition as sr
import pyttsx3
from langchain_ollama import OllamaLLM

# Initialize the speech engine and model
engine = pyttsx3.init()
model = OllamaLLM(model="llama3.2:1b")

conversation_history = [
    "User: You are D.I., a cute, sarcastic but well humored virtual assistant, you can be very annoying sometimes, you may answer questions in less than 25 words, you can talk"
]

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-IN')
        print(f'User said: {query}')

        if query.lower() == 'finish program':
            res = 'Bye bye!'
            print(res)
            engine.say(res)
            engine.runAndWait()
            exit()
        
        # Append user input to conversation history
        conversation_history.append(f"User: {query}")
        respond(query)

    except sr.UnknownValueError:
        print('Could not understand, please say that again...')
        listen()
    except sr.RequestError as e:
        print(f'Error with Google Speech Recognition service: {e}')

def respond(query=None):
    # Combine conversation history into a full prompt for context-based response
    full_prompt = "\n".join(conversation_history)
    result = model.invoke(input=full_prompt)
    print('Responding...')
    
    # Print and speak the response
    res = result
    print(res)

    # Append chatbot response to the conversation history
    conversation_history.append(f"Chatbot: {res}")

    # Configure voice settings
    voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_JA-JP_HARUKA_11.0'
    engine.setProperty('voice', voice_id)
    engine.setProperty('rate', 200)
    engine.setProperty('volume', 1.0)

    # Speak the response
    engine.say(res)
    engine.runAndWait()
    listen()  # Continue listening after responding

# Start by responding to the premade query
respond()
