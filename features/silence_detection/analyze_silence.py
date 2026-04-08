from pydub import AudioSegment, silence


def analyze_silence(audio_path, min_silence_len=500, silence_thresh=-45):
    """
    Analyze an audio file to detect silent segments.

    Returns:
        list of [start_ms, end_ms]
    """

    audio = AudioSegment.from_file(audio_path)

    silences = silence.detect_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )

    return silences