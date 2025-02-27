import os
from moviepy import VideoFileClip, concatenate_videoclips
from artifex.extract_audio.extract_audio import extract_audio
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import detect_nonsilent


def detect_speaking_segments(audio_path, silence_thresh=-35, min_silence_len=1000):
    """
    Detecta os segmentos de áudio onde há fala.
    
    - silence_thresh: Limite de silêncio em decibéis. Mais baixo identifica mais silêncio.
    - min_silence_len: Mínimo de duração do silêncio para considerar uma pausa.
    """
    audio = AudioSegment.from_file(audio_path)
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    # Converte os tempos de milissegundos para segundos
    return [(start / 1000, end / 1000) for start, end in nonsilent_ranges]

def edit_video(video_path, speaking_segments):
    output = f"{os.path.splitext(f'scripts/videos_to_edit/{i}')[0]}_editado.mp4"
    """
    Corta o vídeo com base nos segmentos de fala detectados.
    """
    clip = VideoFileClip(video_path)
    # Extrai os pedaços do vídeo onde há fala
    clips = [clip.subclipped(start, end) for start, end in speaking_segments]
    # Combina todos os clipes em um único vídeo
    final_clip = concatenate_videoclips(clips)
    # Salva o vídeo final
    final_clip.write_videofile(output)
    return output

def main(video_path):
    print("Extraindo áudio do vídeo...")
    audio_path = extract_audio(video_path)

    print("Detectando segmentos com fala...")
    speaking_segments = detect_speaking_segments(audio_path)
    print(f"Segmentos de fala detectados: {speaking_segments}")
    
    print("Editando o vídeo...")
    output = edit_video(video_path, speaking_segments)
    
    print(f"Vídeo editado salvo em: {output}")
    
    # Remove o áudio temporário
    os.remove(audio_path)
    return output

for i in os.listdir("scripts/videos_to_edit"):
   main(f"scripts/videos_to_edit/{i}")
