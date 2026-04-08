import json
import os

file_path = "data/device_data.json"

device_key = os.getenv("DEVICE_KEY")

if not device_key:
    raise ValueError("DEVICE_KEY not set in environment")

DEVICE_MAP = {
    "banjo": "BANJO",
    "sonic": "SONIC",
    "mario": "MARIO",
}

if device_key not in DEVICE_MAP:
    raise ValueError(f"Unknown DEVICE_KEY: {device_key}")

device_name = DEVICE_MAP[device_key]

with open(file_path, "r") as f:
    data = json.load(f)

data["device_name"] = device_name

with open(file_path, "w") as f:
    json.dump(data, f, indent=4)

print(f"[INFO] Runner mapped: {device_key} to {device_name}")