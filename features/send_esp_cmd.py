import requests

def send_command_to_device(ip, state):
    """
    Sends a command (ON/OFF) to the target device via HTTP.
    """
    url = f"http://{ip}/cmd"
    params = {"state": state}
    try:
        response = requests.get(url, params=params)
        print(f"\nCommand sent. Status: {response.status_code}, Response: {response.text}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to send command: {e}\n\nPlease connect with Logi test Wi-Fi router...")
        return False
