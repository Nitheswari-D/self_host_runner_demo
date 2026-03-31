import os
from pydub import AudioSegment


def split_audio(file_path, chunk_duration, output_path, base_filename):
    """
    Splits a WAV audio file into chunks.

    Returns:
        list of chunk file paths
    """

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    audio = AudioSegment.from_wav(file_path)

    duration_ms = len(audio)
    chunk_duration_ms = chunk_duration * 1000

    chunk_paths = []

    for start_ms in range(0, duration_ms, chunk_duration_ms):

        chunk = audio[start_ms:start_ms + chunk_duration_ms]

        chunk_filename = f"{base_filename}_part_{start_ms // chunk_duration_ms + 1}.wav"
        chunk_path = os.path.join(output_path, chunk_filename)

        chunk.export(chunk_path, format="wav")

        print(f"Saved chunk: {chunk_path}")

        chunk_paths.append(chunk_path)

    return chunk_paths