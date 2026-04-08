import time
import requests

def wait_for_esp(ip, timeout=10):
    start = time.time()

    while time.time() - start < timeout:
        try:
            r = requests.get(f"http://{ip}", timeout=2)
            print("ESP is ready!")
            return True
        except:
            print("Waiting for ESP...")
            time.sleep(1)

    return False