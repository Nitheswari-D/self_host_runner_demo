import sounddevice as sd

def list_input_devices():
    """
    Function description: This function will lists all available audio input devices on the system.
    """

    print("\n Available Input Devices:")
    devices = sd.query_devices()
    input_devices = [dev for dev in devices if dev['max_input_channels'] > 0]
    for idx, dev in enumerate(input_devices):
        print(f"{idx}: {dev['name']}")
    return input_devices