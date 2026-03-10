import os
import json
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
