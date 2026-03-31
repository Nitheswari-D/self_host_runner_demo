import sounddevice as sd
import soundfile as sf


def play_audio_async(playback_file, device_name=None):
    data, samplerate = sf.read(playback_file)

    if device_name:
        devices = sd.query_devices()
        for idx, dev in enumerate(devices):
            if dev['max_output_channels'] > 0 and device_name.lower() in dev['name'].lower():
                print(f" Playing on: {dev['name']}")
                sd.play(data, samplerate, device=idx)
                return
        raise Exception(f"Output device '{device_name}' not found")

    sd.play(data, samplerate)