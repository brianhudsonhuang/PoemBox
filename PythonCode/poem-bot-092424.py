
import numpy as np
import os
import serial
import sounddevice as sd
import sys
import tempfile
import time
import warnings
from pynput import keyboard
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
from openai import OpenAI
from pathlib import Path
from playsound import playsound 

warnings.filterwarnings("ignore", category=DeprecationWarning)

class WhisperTranscriber:
    def __init__(self, model_size="large-v3", sample_rate=44100):
        self.model_size = model_size
        self.sample_rate = sample_rate
        self.model = WhisperModel(model_size, device="cuda", compute_type="float16")                                                           
        self.is_recording = False

    def on_press(self, key):
        if key == keyboard.Key.space:
            if not self.is_recording:
                self.is_recording = True
                print("Recording started.")
        
    def on_release(self, key):
        if key == keyboard.Key.space:
            if self.is_recording:
                self.is_recording = False
                print("Recording stopped.")
                return False
                    
    def record_audio(self):
        recording = np.array([], dtype='float64').reshape(0, 2)
        frames_per_buffer = int(self.sample_rate * 1)

        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            while True:
                if self.is_recording:
                    chunk = sd.rec(frames_per_buffer, samplerate=self.sample_rate, channels=2, dtype='float64')
                    sd.wait()
                    recording = np.vstack([recording, chunk])
                if not self.is_recording and len(recording) > 0:
                    break
            listener.join()
        
        return recording
    
    def save_temp_audio(self, recording):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        write(temp_file.name, self.sample_rate, recording)
        return temp_file.name
    
    def transcribe_audio(self, file_path):
        segments, info = self.model.transcribe(file_path, beam_size=5)
        print ("Detect language '%s' with probability %f" % (info.language, info.language_probability))
        full_transcription = ""
        for segment in segments:
            # print(segment.text)
            full_transcription += segment.text + " "
        os.remove(file_path)
        return full_transcription

def run(secretRecording, _assistant):
    print ("Hold the spacebar to start recording...")
    try:
        while True:
            
            recording = secretRecording.record_audio()
            file_path = secretRecording.save_temp_audio(recording)
            thread = client.beta.threads.create()
            secretTranscription = secretRecording.transcribe_audio(file_path)
            print(secretTranscription)
            messages = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=secretTranscription,
            )
            assistant_run = client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=_assistant.id,
                instructions="Please write a very very short poem about the secret the user submitted"
            )
            if assistant_run.status == 'completed': 
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                poem = messages.data[0].content[0].text.value
                print(poem)
                speech_file_path = Path(__file__).parent / "speech.mp3"
                response = client.audio.speech.create(
                    model="tts-1",
                    voice="onyx",                  
                    input=poem,
                )
                arduino.write(b'1')
                response.stream_to_file(speech_file_path)
                while True:
                    while (arduino.inWaiting()==0):
                        pass
                    dataPacket=arduino.readline()
                    dataPacket=str(dataPacket,'utf-8')
                    dataPacket=dataPacket.strip('\r\n')
                    if (dataPacket == "TOP OPEN"):
                        print(dataPacket)
                        playsound('speech.mp3')
                        os.remove('speech.mp3')
                        arduino.write(b'0')
                        break
            else:
                print(assistant_run.status)
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
        

if __name__ == "__main__":

    OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key = OPEN_AI_API_KEY)
    #instantiate arduino
    arduino = serial.Serial('COM6',115200)
    #wait for arduino to initialize
    time.sleep(1)

    assistant = client.beta.assistants.create(
        name="Poem Assistant",
        instructions="You are a poet that is told a secret. Write a short poem about the main themes in the secret",
        # tools=[{"type": "code_interpreter"}],
        model="gpt-4-turbo-preview",
    )

    transcriber = WhisperTranscriber()
    run(transcriber, assistant)
