import hid
from data.config_data import DEVICE_NAME
from features.config_loader import DEV_NAME

def find_dut():
    LOGI_VID = DEVICE_NAME[DEV_NAME]["vid"]
    DEVICE_PID = DEVICE_NAME[DEV_NAME]["pid"]
    USAGE_PAGE = DEVICE_NAME[DEV_NAME]["usage_pg"]
    print("variables enumerated")
    device_path = ""
    for d in hid.enumerate(LOGI_VID, DEVICE_PID):
        if d.get('usage_page') == USAGE_PAGE:
            device_path = d.get('path')
    print("Device path in find_dut", device_path)
    return device_path

def open_device():
    device_path = find_dut()
    if not device_path:
        raise RuntimeError("Device not found. Check VID, PID, Usage Page")
    print("device path in open_device", device_path)
    device = hid.device()
    device.open_path(device_path)
    return device