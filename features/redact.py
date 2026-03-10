import json
import re
import time
import os
import subprocess
import pyautogui

pyautogui.FAILSAFE = True
CONFIG_FILE = "data/config.json"

# ------------------ helpers ------------------

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def wait(sec=1.5):
    time.sleep(sec)


def extract_fw_version(dfu_path):
    """
    Extract firmware version from DFU filename
    Example:
    BanjoHeadset_1.1_build2425_signed_prod.bin
    -> 1.1_build2425
    """
    name = os.path.basename(dfu_path)
    match = re.search(r'(\d+\.\d+_build\d+)', name, re.IGNORECASE)
    return match.group(1) if match else None


# ROBUST redacted EXE detection (cross-machine safe)
def wait_for_redacted_exe(folders, timeout):
    print("\n Waiting for redacted EXE to be created...")
    start = time.time()

    while time.time() - start < timeout:
        for folder in folders:
            if not os.path.exists(folder):
                continue

            for f in os.listdir(folder):
                fname = f.lower()
                if fname.endswith(".exe") and ("redact" in fname or "dfu" in fname):
                    full_path = os.path.join(folder, f)
                    try:
                        size1 = os.path.getsize(full_path)
                        time.sleep(0.5)
                        size2 = os.path.getsize(full_path)
                        if size1 == size2:
                            return full_path
                    except OSError:
                        pass

        time.sleep(1)

    return None


def select_usb_product(cfg):
    active_key = cfg.get("active_product")
    products = cfg.get("products", {})

    if not active_key or active_key not in products:
        print(" Active product not defined or invalid in config")
        return False

    product = products[active_key]
    index = product["index"]
    name = product["display"]

    print(f"\n Selecting USB product: {name} (index {index})")

    # Allow CentPP list to fully render
    time.sleep(2.5)

    # HARD reset cursor to top
    for _ in range(60):
        pyautogui.press("up")
        time.sleep(0.03)

    # Move down to correct index
    for _ in range(index):
        pyautogui.press("down")
        time.sleep(0.06)

    pyautogui.press("enter")
    print(" USB product selected")
    return True


# ------------------ main flow ------------------

def redact():
    cfg = load_config()

    centpp = cfg["centpp_exe"]
    output_dir = cfg["output_dir"]
    dfu_bin = cfg["dfu_file"]
    usb_timeout = cfg.get("usb_select_timeout_sec", 180)
    auto_launch = cfg.get("auto_launch_redacted_exe", True)
    force_fw = cfg.get("force_fw_version_entry", False)

    if not os.path.exists(centpp):
        print("CentPP EXE not found")
        return

    if not os.path.exists(dfu_bin):
        print("DFU BIN not found:", dfu_bin)
        return

    print(" Launching CentPP (new console)...")
    centpp_proc = subprocess.Popen(
        centpp,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    wait(4)

    print(" Selecting Redact (R)")
    pyautogui.press("r")
    wait(2)

    print(" Accepting source EXE")
    pyautogui.press("enter")
    wait(3)

    print(" Providing output folder")
    pyautogui.write(output_dir, interval=0.02)
    pyautogui.press("enter")
    wait(3)

    if cfg.get("dfu_only", True):
        print("DFU_ONLY selected")
        pyautogui.press("enter")
        wait(2)

    print(" Providing DFU bin path")
    pyautogui.write(dfu_bin, interval=0.02)
    pyautogui.press("enter")
    wait(2)

    fw_version = extract_fw_version(dfu_bin)
    wait(1.5)

    if fw_version:
        print(f"Typing firmware version: {fw_version}")
        pyautogui.write(fw_version, interval=0.02)

    pyautogui.press("enter")

    # ---------- USB product selection ----------
    if not select_usb_product(cfg):
        centpp_proc.terminate()
        return

    # ---------- Wait for redacted EXE ----------
    centpp_dir = os.path.dirname(centpp)

    redacted_exe = wait_for_redacted_exe(
        folders=[output_dir, centpp_dir],
        timeout=usb_timeout
    )

    if not redacted_exe:
        print("\n FAILED: Redacted EXE not created")
        centpp_proc.terminate()
        return

    print("\n Redacted EXE created successfully:")
    print(redacted_exe)

    print("Closing CentPP")
    centpp_proc.terminate()

    if auto_launch:
        print("Launching redacted EXE (DFU)...")
        process = subprocess.Popen(
            redacted_exe,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )
        process.wait()

    print("\nDFU started successfully")
    print("Flow complete")
    return True

