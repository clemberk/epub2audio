
import os
import uuid
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
elevenlabs = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)


def text_to_speech_file(text: str) -> str:
    response = elevenlabs.text_to_speech.convert(
        voice_id="NBqeXKdZHweef6y0B67V", # Christian Voice
        output_format="mp3_44100_128",
        text=input_text,
        model_id="eleven_flash_v2_5", # flash model for low latency
    )

    save_file_path = f"{chapter_num}.mp3"

    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    return save_file_path

