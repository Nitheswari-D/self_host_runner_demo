import os
import json
import serial
import serial.tools.list_ports
import re
import time
from data.config_data import DEVICE_NAME


def read_device_info(device_info_file_path):
    if not os.path.exists(device_info_file_path):
        raise FileNotFoundError(
            f"Device info file does not exist at {device_info_file_path}"
        )

    with open(device_info_file_path, "r") as f:
        return json.load(f)


def setup_device(context, raw_name):
    raw_name = raw_name.strip().upper()

    device_info = DEVICE_NAME.get(raw_name)
    if not device_info:
        raise ValueError(f"No mapping found for device '{raw_name}'")

    context["device"] = {
        "raw_name": raw_name,
        "name": device_info["audio_name"],
        "vid": device_info["vid"],
        "pid": device_info["pid"],
        "usage_pg": device_info["usage_pg"],
        "state": device_info["state"],
    }

    return True


def find_esp_port():
    ports = serial.tools.list_ports.comports()

    for port in ports:
        print(f"Checking: {port.device} - {port.description}")

        if "CP210x" in port.description:
            print(f"ESP32 found on {port.device}")
            return port.device

    raise Exception("ESP32 not found")


def get_esp_ip():
    port = find_esp_port()

    ser = serial.Serial(port, 115200, timeout=2)

    ser.setDTR(False)
    time.sleep(0.5)
    ser.setDTR(True)

    print("Waiting for IP log...")

    start_time = time.time()

    while True:
        line = ser.readline().decode(errors="ignore").strip()

        if line:
            print(line)

        if "WIFI_INIT: Got IP:" in line:
            ip = re.search(r"\d+\.\d+\.\d+\.\d+", line).group()
            print(f"\nESP32 IP Detected: {ip}")
            return ip

        if time.time() - start_time > 20:
            raise Exception("Failed to get IP from ESP32")