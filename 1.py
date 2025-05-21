
import streamlit as st
import speech_recognition as sr
import pyttsx3
from deep_translator import GoogleTranslator
import threading


engine = pyttsx3.init()


engine_lock = threading.Lock()

def listen_to_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        st.info("Recognizing...")
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        return f"Error connecting to Google: {e}"

def translate_text(text, dest_language):
    try:
        translated = GoogleTranslator(source='auto', target=dest_language).translate(text)
        return translated
    except Exception as e:
        return f"Translation error: {e}"


def speak(text):
    def run_speech():
        with engine_lock:
            engine.say(text)
            engine.runAndWait()

    threading.Thread(target=run_speech).start()


st.title("🎤 Voice-to-Voice Translator")
st.write("Speak something, and I'll translate and say it back!")

language_code = st.chat_input("Enter target language code (e.g., 'es' for Spanish, 'fr' for French):")

if st.button("🎙️ Start Recording"):
    spoken_text = listen_to_speech()
    st.success(f"You said: {spoken_text}")

    if language_code:
        translated = translate_text(spoken_text, language_code)
        st.success(f"Translated text: {translated}")
        speak(translated)  
    else:
        st.warning("Please enter a target language code.")
