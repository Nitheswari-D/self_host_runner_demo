import json
import os
import pytest

from features.silence_detection.run_silence_detection import run_silence_detection
from features.silence_detection.list_devices import list_input_devices

# def load_config():
#     config_path = os.path.join(
#         os.path.dirname(__file__),
#         "..",
#         "data",
#         "silence_detection_config.json"
#     )

#     with open(config_path, "r") as f:
#         return json.load(f)


def load_config():
    with open("data/silence_detection_config.json") as f:
        config = json.load(f)

    with open("data/device_data.json") as f:
        device_data = json.load(f)

    device_name = device_data["device_name"]

    if device_name not in config["devices"]:
        raise Exception(f"Device '{device_name}' not found in config")

    # 🔥 Merge common + device-specific
    final_config = config["common"].copy()
    final_config.update(config["devices"][device_name])

    print(f"\n📱 Running for device: {device_name}")

    return final_config


def get_device_index(devices, device_name):
    for device in devices:
        if device_name.lower() in device["name"].lower():
            print(f"\n Selected Device: {device['name']}")
            return device["index"]

    raise Exception(f" Device '{device_name}' not found")

def test_silence_detection():

    config = load_config()

    mic_name = config["mic_name"]
    base_dir = config["base_dir"]
    duration = config["duration"]
    chunk_duration = config["chunk_duration"]
    playback_file = config["playback_file"]
    playback_device = config["playback_device"]

    print("\n=== Listing Input Devices ===")
    devices = list_input_devices()

    mic_index = get_device_index(devices, mic_name)
    playback_device_index = get_device_index(devices, playback_device)

    print("\n=== Running Silence Detection Test ===")

    result = run_silence_detection(
        mic_name=mic_name,
        mic_index=mic_index,
        base_dir=base_dir,
        duration=duration,
        chunk_duration=chunk_duration,
        playback_file=playback_file,
        playback_device=playback_device,
        playback_device_index=playback_device_index
    )

    assert result is True, "Mic recording or processing failed"