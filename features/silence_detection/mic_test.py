import sounddevice as sd
import wave
import time
import os
import sys

from pydub import AudioSegment, silence
from features.silence_detection.audio_playback import play_audio_async
from features.silence_detection.audio_stream_handler import play_and_record
from features.silence_detection.play_and_record_thread import play_and_record_thread


def record_audio(device_index, filename, duration):
    """
    Records audio from the specified input device and saves it as a WAV file.
    """

    input_info = sd.query_devices(device_index)
    print(f"\n Selected Input Device: {input_info['name']}")

    samplerate = 48000

    print(f"Recording for {duration} seconds...")
    recording = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype='int16',
        device=device_index
    )

    sd.wait()
    print("Recording complete.")

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 2 bytes
        wf.setframerate(samplerate)
        wf.writeframes(recording.tobytes())

    print(f"Audio saved to: {filename}")


def mic_test(device_name, device_index, filename, duration, playback_file, playback_device, playback_device_index, min_silence_len=150, silence_thresh=-40):
    """
    Validates mic by recording a short sample and checking for sound.
    If sound is detected → proceeds with full recording.
    """

    try:
        # Reset audio backend
        sd._terminate()
        sd._initialize()

        print("\n Waiting 20 seconds for device initialization...")
        time.sleep(20)

        test_filename = "mic_test.wav"

        # Start playback (NON-BLOCKING)
        # if playback_file:
        #     play_audio_async(playback_file=playback_file, device_name=playback_device)
        #     time.sleep(1)  

        # # Short test recording
        # record_audio(device_index=device_index, filename=test_filename, duration=10)

        # play_and_record(
        #     playback_file= playback_file,
        #     output_device_name= playback_device,
        #     input_device_name=device_name,
        #     duration=10,
        #     output_wav=test_filename
        # )

        play_and_record_thread(
            input_id=device_index,
            output_id=playback_device_index,
            audio_file=playback_file,
            output_file=test_filename
        )


        print("\nAnalyzing mic test recording for sound activity...")

        audio = AudioSegment.from_wav(test_filename)

        nonsilent_ranges = silence.detect_nonsilent(
            audio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh
        )

        if nonsilent_ranges:
            print("Mic test passed. Proceeding with full recording...")

            # Full recording
            record_audio(
                device_index=device_index,
                filename=filename,
                duration=duration
            )

        else:
            print("Mic test failed. No sound detected.")
            raise Exception("Mic test failed: No sound detected")

        # Cleanup
        if os.path.exists(test_filename):
            os.remove(test_filename)

    except Exception as e:
        print(f"\n Error in mic_test: {e}")
        raise   