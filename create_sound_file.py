from kokoro import KModel, KPipeline
import soundfile as sf
import torch

pipeline = KPipeline(lang_code='d') 

text = "Dies ist ein Test der deutschen Sprachausgabe. Das Projekt mit dem E-Pub File nimmt Gestalt an."


# voice = 'de_nicole'
voice = 'de_leo'

generator = pipeline(
    text, voice=voice, 
    speed=1.1, split_pattern=r'\n+' 
)

for i, (gs, ps, audio) in enumerate(generator):
    sf.write(f'kapitel_test_{i}.wav', audio, 24000) 
    print(f"Teil {i} wurde generiert.")

print("Fertig!")