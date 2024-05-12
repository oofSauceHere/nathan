# still a rough draft

import time
import re
import os
from tempfile import TemporaryFile
from playsound import playsound
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer

# > should catch errors and exit program
# called every time audio is detected, and pulls "er" words from the transcript
def callback(recognizer, audio):
    try:
        words = recognizer.recognize_whisper(audio, language="en").lower()
        ls = re.findall("\\w*(?:er)\\b", words) # "\\w*(?:er|r|re)\\b"
        if(len(ls) > 0):
            print(ls[-1])
            tts = gTTS(text=f"{ls[-1]}? I hardly know her!", lang='en')
            tts.save("lol.mp3")

            # initializes pygame audio mixer to speak into virtual audio cable (which will output into microphone)
            mixer.init(devicename="CABLE Input (VB-Audio Virtual Cable)")
            mixer.music.load("lol.mp3")
            mixer.music.play()

            # if we quit without waiting, we can't delete the audio file
            time.sleep(5)
            mixer.quit()
            # playsound("lol.mp3")

            # for some reason, gtts won't open existing files, so we need to recreate the audio file every function call
            os.remove("lol.mp3")
    except sr.UnknownValueError:
        print("couldn't understand")
    except sr.RequestError as e:
        print(f"couldn't request, {e}")
    except:
        exit(1)

def main():
    try:
        os.remove("lol.mp3")
    except FileNotFoundError:
        print("no audio file exists")

    # sets up speech recognizer and microphone input
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=sr.Microphone.list_microphone_names().index("Voicemeeter Out B1 (VB-Audio Vo"))
    # mic = sr.Microphone()

    # MIC DEBUGGING

    # i = 0
    # default_mic = "Voicemeeter AUX Input (VB-Audio Voicemeeter VAIO)"
    # for index, name in enumerate(sr.Microphone.list_microphone_names()):
    #     # print(name)
    #     if(default_mic == name):
    #         i = index
    #         break
    # mic = sr.Microphone(device_index=i)

    # tailors model to ignore ambient noise
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

        # for one-time transcription
        # print("talk")
        # audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)

    # runs listener in a separate thread
    stop_listening = recognizer.listen_in_background(mic, callback, phrase_time_limit=5)
    print("running !!")

    # consider transcribing the text outside of the callback function so you have greater control over effectiveness

    # keep going forever!!
    while True:
        time.sleep(0.1)



    # UNNECESSARY

    # stop_listening(wait_for_stop=False)

    # with open("microphone-results.wav", "wb") as f:
    #     print("you talked")
    #     f.write(audio.get_wav_data())

    # try:
    #     print("you said: " + recognizer.recognize_whisper(audio, language="english"))
    # except sr.UnknownValueError:
    #     print("couldn't understand")
    # except sr.RequestError as e:
    #     print(f"couldn't request, {e}")

if __name__ == "__main__":
    main()