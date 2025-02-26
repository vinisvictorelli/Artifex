from moviepy import VideoFileClip, concatenate_videoclips

def extract_audio(video_path):
    """
    Extrai o áudio de um vídeo e salva como um arquivo temporário.
    """
    clip = VideoFileClip(video_path)
    audio_path = "tmp/temp_audio.wav"
    clip.audio.write_audiofile(audio_path, codec="pcm_s16le")
    return audio_path