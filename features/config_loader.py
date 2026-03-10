import json

with open("data/device_data.json", "r") as f:
    device_data = json.load(f)

DEV_NAME = device_data["device_name"]
DEVICE_NAME_LOWER = DEV_NAME.lower()
BUILD_VERSION = device_data["build_version"]