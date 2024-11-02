import wave
import struct
import time
import pyttsx3
import speech_recognition as sr
import pywhatkit
from pvrecorder import PvRecorder
from Configuration.config import saved_audio_path

from email_test.send_mail import send_mail_to_test_beta

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()


devices = PvRecorder.get_available_devices()
for index, device in enumerate(devices):
    print(f"Device {index}: {device}")

# Recorder settings
recorder = PvRecorder(device_index=0, frame_length=4096)
audio = []
path = saved_audio_path

try:
    recorder.start()
    
    start_time = time.time()
    duration = 8

    print("Recording started...")
    while True:
        frame = recorder.read()
        audio.extend(frame)
        
        if time.time() - start_time >= duration:
            print("Recording stopped after 5 seconds.")
            break

except KeyboardInterrupt:
    print("Recording interrupted by user.")
finally:
    recorder.stop()
    with wave.open(path, 'w') as f:
        f.setparams((1, 2, 16000, len(audio), "NONE", "NONE"))
        f.writeframes(struct.pack("h" * len(audio), *audio))
    recorder.delete()
    print(f"Audio saved to {path}")


recognizer = sr.Recognizer()
text = ""
try:
    with sr.AudioFile(path) as source:
        print("Converting speech to text...")
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        print(f"Recognized Text: {text}")
        speak(f"You said: {text}")
except sr.UnknownValueError:
    print("Could not understand the audio.")
    speak("Sorry, I could not understand the audio.")
except sr.RequestError:
    print("Error with the speech recognition service.")
    speak("There was an error with the speech recognition service.")


def execute_command(text):
    if "send email" in text:
        print('Sending mail...')
        speak('Sending mail to test BETA MALE..')
        send_mail_to_test_beta()
    
    if "play music" in text:
        song = text.split("play music", 1)[1].strip()
        if song:
            print(f"Playing {song} on YouTube...")
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song) 
        else:
            speak("Please specify a song name.")



if text:
    execute_command(text)
