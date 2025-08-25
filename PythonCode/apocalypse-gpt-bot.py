
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

# warnings.filterwarnings("ignore", category=DeprecationWarning)

def run(client):
    try:
        messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]
        while True:
            message = input("User : ")
            if message:
                messages.append(
                    {"role": "user", "content": message},
                )
                chat = client.chat.completions.create(
                    model="gpt-4-turbo", messages=messages
                )
            reply = chat.choices[0].message.content
            print(f"ChatGPT: {reply}")
            messages.append({"role": "assistant", "content": reply})

    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)

if __name__ == "__main__":

    OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key = OPEN_AI_API_KEY)
    run(client)

    #instantiate arduino
    # arduino = serial.Serial('COM7',9600)
    #wait for arduino to initialize

    # while True:
    #     dataPacket = arduino.readline()
    #     dataPacket=str(dataPacket,'utf-8')
    #     dataPacket=dataPacket.strip('\r\n')
    #     if (dataPacket == "TOUCH"):
    #         print(dataPacket)
