from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os
import soundfile as sf
import torch

load_dotenv()

elevenlabs = ElevenLabs(
    api_key = os.getenv("ELEVENLABS_API_KEY")
)

audio = elevenlabs.text_to_speech.convert(
    text="Dies ist ein Test der deutschen Sprachausgabe. Das Projekt mit dem E-Pub File nimmt Gestalt an.",
    voice_id="NBqeXKdZHweef6y0B67V",
    model_id="eleven_v3",
    output_format="mp3_44100_128"
)

play(audio)