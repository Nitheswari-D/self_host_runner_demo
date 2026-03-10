import json
import re
import time
import os
import pyautogui

pyautogui.FAILSAFE = True
CONFIG_FILE = r"data\config.json"


def load_config():
    """Load the configuration JSON file."""
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def wait(sec=1.5):
    """Sleep helper."""
    time.sleep(sec)


def extract_fw_version(dfu_path):
    """Extract firmware version from DFU filename."""
    name = os.path.basename(dfu_path)
    match = re.search(r'(\d+\.\d+_build\d+)', name, re.IGNORECASE)
    return match.group(1) if match else "unknown"


def get_build_output_dir(base_dir, dfu_bin):
    """Create output folder for the redacted EXE."""
    fw = extract_fw_version(dfu_bin)
    folder = f"{fw}_redacted_build"
    out = os.path.join(base_dir, folder)
    os.makedirs(out, exist_ok=True)
    return out


def wait_for_redacted_exe(folder, timeout):
    """Wait for the redacted EXE to be generated."""
    print("\n Waiting for redacted EXE to be created...")
    start = time.time()

    while time.time() - start < timeout:
        if os.path.exists(folder):
            for f in os.listdir(folder):
                fname = f.lower()
                if fname.endswith(".exe") and ("redact" in fname or "dfu" in fname):
                    full = os.path.join(folder, f)
                    try:
                        s1 = os.path.getsize(full)
                        time.sleep(0.5)
                        s2 = os.path.getsize(full)
                        if s1 == s2:
                            return full
                    except OSError:
                        pass
        time.sleep(1)
    return None


def select_usb_product(cfg):
    """Select the USB product using pyautogui."""
    active_key = cfg.get("active_product")
    products = cfg.get("products", {})

    if not active_key or active_key not in products:
        print(" Active product not defined or invalid")
        return False

    product = products[active_key]
    index = product["index"]
    name = product["display"]

    print(f"\n Selecting USB product: {name} (index {index})")

    time.sleep(2.5)
    for _ in range(60):
        pyautogui.press("up")
        time.sleep(0.03)
    for _ in range(index):
        pyautogui.press("down")
        time.sleep(0.06)

    pyautogui.press("enter")
    return True