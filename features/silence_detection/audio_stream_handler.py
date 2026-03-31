import sounddevice as sd
import soundfile as sf
import numpy as np
import wave
import time


def get_device_index(device_name, is_input=True):
    devices = sd.query_devices()

    for idx, dev in enumerate(devices):
        if is_input and dev['max_input_channels'] > 0:
            if device_name.lower() in dev['name'].lower():
                print(f" Selected Input: {dev['name']}")
                return idx

        if not is_input and dev['max_output_channels'] > 0:
            if device_name.lower() in dev['name'].lower():
                print(f" Selected Output: {dev['name']}")
                return idx

    raise Exception(f"Device '{device_name}' not found")


def play_and_record(playback_file,
                    output_device_name,
                    input_device_name,
                    duration,
                    output_wav):

    # 🔹 Load playback audio
    data, samplerate = sf.read(playback_file)

    if len(data.shape) > 1:
        data = data[:, 0]  # mono

    # 🔹 Get device indices
    out_dev = get_device_index(output_device_name, is_input=False)
    in_dev = get_device_index(input_device_name, is_input=True)

    # 🔹 Recording buffer
    recording = []

    # 🔊 Output callback
    def output_callback(outdata, frames, time_info, status):
        nonlocal data
        if status:
            print(f"Output status: {status}")

        chunk = data[:frames]
        outdata[:len(chunk), 0] = chunk

        if len(chunk) < frames:
            outdata[len(chunk):] = 0  # pad silence
        data = data[frames:]

    # 🎙️ Input callback
    def input_callback(indata, frames, time_info, status):
        if status:
            print(f"Input status: {status}")

        recording.append(indata.copy())

    print("\n Starting parallel playback + recording...")

    # 🔥 Create streams
    with sd.OutputStream(
        samplerate=samplerate,
        device=out_dev,
        channels=1,
        callback=output_callback
    ), sd.InputStream(
        samplerate=samplerate,
        device=in_dev,
        channels=1,
        callback=input_callback
    ):

        time.sleep(duration)  # ⏱️ run both streams

    print(" Streams finished")

    # 🔹 Convert recording buffer
    audio_data = np.concatenate(recording, axis=0)

    # 🔹 Save WAV
    with wave.open(output_wav, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # int16
        wf.setframerate(samplerate)
        wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())

    print(f" Recorded file saved: {output_wav}")