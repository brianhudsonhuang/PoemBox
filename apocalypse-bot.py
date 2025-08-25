
import numpy as np
import os
import serial
import sounddevice as sd
import sys
import tempfile
import time
import warnings
from scipy.io.wavfile import write
from openai import OpenAI
from pathlib import Path
from playsound import playsound 

warnings.filterwarnings("ignore", category=DeprecationWarning)

def run():
    try:
        while True:
            # while (arduino.inWaiting()==0):
            dataPacket=arduino.readline()
            dataPacket=str(dataPacket, 'utf-8')
            dataPacket=dataPacket.strip('\r\n')
            if (dataPacket == "TOUCH"):
                print(dataPacket)
                thread = client.beta.threads.create()
                messages = client.beta.threads.messages.create(
                    thread_id = thread.id,
                    role = "user",
                    content = "Lack of Oxygen (Hypoxia), Decompression, Boiling of Body Fluids, Radiation Exposure, Temperature Extremes, Loss of Pressure on Gases (Ebullism)"
                    )  
                run = client.beta.threads.runs.create_and_poll(
                    thread_id=thread.id,
                    assistant_id=assistant.id,
                    instructions="Randomly choose one effect from the list given by the user. Make sure not to repeat the previous one. Describe in extreme detail how that effect occurs to the human body while in space without protection. Do not provide commentary. Imitate the tone of a textbook. Include facts, figures, and statistics. Limit to 200 words. Write in paragraph format."
                    )
                if run.status == 'completed':
                    messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                    )
                    text = messages.data[0].content[0].text.value
                    print(text)
                    arduino.write(b'1')
                    #     speech_file_path = Path(__file__).parent / "text.mp3"
                    #     response = client.audio.speech.create(
                    #         model="tts-1",
                    #         voice="onyx",                  
                    #         input=text,
                    #         )
                    #     response.stream_to_file(speech_file_path)
                    #     playsound('text.mp3')
                    #     os.remove('text.mp3')
                    break

                else:
                    print(run.status)

    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)

if __name__ == "__main__":

    OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key = OPEN_AI_API_KEY)
   
    #instantiate arduino
    arduino = serial.Serial('COM7',9600)
    #wait for arduino to initialize

    assistant = client.beta.assistants.create(
        name="Apocalypse Assistant",
        instructions="You are a scientist that is an expert in space biology.",
        model="gpt-4-turbo-preview",
    )

    run()