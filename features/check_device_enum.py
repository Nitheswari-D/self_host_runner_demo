import sounddevice as sd
import threading

thread_lock = threading.Lock()

def check_device(device_name):
    """
    Checks if a given device is connected/enumerated in the list of audio devices.
    """
    with thread_lock:
        try:
            sd._terminate()
            sd._initialize()
            devices = sd.query_devices()
            device_name = device_name.lower()
            for device in devices:
                name = device["name"].lower()
                # Ignore WDM-KS (fake endpoints)
                if device["hostapi"] == 3:
                    continue

                # Ignore Hands-Free Bluetooth profile
                if "hands-free" in name:
                    continue
                #print("\nChecking:", device["name"])
                #print("Match? →", device_name in name)
                if device_name in name:
                    print("Real device matched!")
                    return True
            return False
        except Exception as e:
            print(f"The error is {e}")
            return False
        
        
