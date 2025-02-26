import whisper
import os
from math import ceil

def mp3_to_srt(mp3_file: str, max_chars_per_segment: int = 42):
    """
    Converte um arquivo MP3 em um arquivo de legendas SRT com segmentos ajustados
    por quantidade máxima de caracteres.

    Args:
        mp3_file (str): Caminho do arquivo MP3.
        output_srt (str): Caminho para salvar o arquivo SRT gerado.
        max_chars_per_segment (int): Número máximo de caracteres por segmento.
    """
    # Carregar o modelo Whisper
    model = whisper.load_model("medium")  # Escolha entre "tiny", "base", "small", "medium", "large"

    print("Transcrevendo o arquivo de áudio...")
    # Transcrição
    result = model.transcribe(mp3_file, language="pt")

    print("Gerando arquivo SRT...")
    # Extrair legendas no formato SRT
    with open("tmp/legenda.srt", 'w', encoding='utf-8') as srt_file:
        index = 1
        for segment in result['segments']:
            start = segment['start']
            end = segment['end']
            text = segment['text']

            # Dividir o texto com base no número máximo de caracteres
            split_text = split_text_by_chars(text, max_chars_per_segment)
            segment_duration = (end - start) / len(split_text)  # Dividir duração igualmente

            # Escrever cada parte no arquivo SRT com tempos ajustados
            for i, part in enumerate(split_text):
                part_start = start + i * segment_duration
                part_end = part_start + segment_duration

                # Formatar o tempo no estilo SRT
                start_time = format_timestamp(part_start)
                end_time = format_timestamp(part_end)

                # Escrever no arquivo
                srt_file.write(f"{index}\n")
                srt_file.write(f"{start_time} --> {end_time}\n")
                srt_file.write(f"{part}\n\n")
                index += 1

    print(f"Arquivo SRT gerado com sucesso")

def split_text_by_chars(text: str, max_chars: int) -> list:
    """
    Divide um texto em partes com no máximo `max_chars` caracteres,
    garantindo que palavras não sejam cortadas.

    Args:
        text (str): Texto a ser dividido.
        max_chars (int): Número máximo de caracteres por parte.

    Returns:
        list: Lista de partes do texto.
    """
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        # Verificar se a linha atual com a nova palavra excede o limite
        if len(" ".join(current_line + [word])) <= max_chars:
            current_line.append(word)
        else:
            # Adicionar a linha atual à lista e começar uma nova
            lines.append(" ".join(current_line))
            current_line = [word]

    # Adicionar a última linha, se existir
    if current_line:
        lines.append(" ".join(current_line))

    return lines

def format_timestamp(seconds: float) -> str:
    """
    Converte tempo em segundos para o formato SRT (hh:mm:ss,ms).

    Args:
        seconds (float): Tempo em segundos.

    Returns:
        str: Tempo formatado no estilo SRT.
    """
    millis = int(seconds * 1000)
    hours = millis // 3600000
    millis %= 3600000
    minutes = millis // 60000
    millis %= 60000
    seconds = millis // 1000
    millis %= 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"

mp3_to_srt("scripts/ram_dual_channel.mp3",30)
