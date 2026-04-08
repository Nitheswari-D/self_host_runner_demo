import sounddevice as sd
import numpy as np
import threading
import wave
import soundfile as sf
from scipy.signal import resample
from scipy.io import wavfile
import os

CHANNELS = 1


def play_and_record_thread(input_id, output_id, audio_file, output_file):
    # -------- LOAD AUDIO --------
    if not os.path.exists(audio_file):
        raise Exception(f"Audio file not found: {audio_file}")

    try:
        audio, samplerate = sf.read(audio_file)
    except Exception:
        samplerate, audio = wavfile.read(audio_file)
        audio = audio.astype('float32') / 32767

    # Convert stereo → mono
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)

    # -------- MATCH DEVICE SAMPLE RATE --------
    device_info = sd.query_devices(output_id, 'output')
    device_samplerate = int(device_info['default_samplerate'])

    if samplerate != device_samplerate:
        duration = len(audio) / samplerate
        new_length = int(duration * device_samplerate)
        audio = resample(audio, new_length)
        samplerate = device_samplerate

    duration = len(audio) / samplerate

    # -------- RECORDING BUFFER --------
    recorded = []

    # -------- RECORD THREAD --------
    def record_stream():
        def callback(indata, frames, time, status):
            if status:
                print("⚠️", status)
            recorded.append(indata.copy())

        with sd.InputStream(
            samplerate=samplerate,
            channels=CHANNELS,
            callback=callback,
            device=input_id
        ):
            sd.sleep(int(duration * 1000))

    # Start recording
    t = threading.Thread(target=record_stream)
    t.start()

    # -------- PLAY AUDIO --------
    sd.play(audio, samplerate=samplerate, device=output_id)

    # Wait for recording to finish
    t.join()

    # -------- SAVE FILE --------
    if not recorded:
        raise Exception("Recording failed: no data captured")

    recorded_audio = np.concatenate(recorded, axis=0)

    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes((recorded_audio * 32767).astype(np.int16).tobytes())

    return output_file