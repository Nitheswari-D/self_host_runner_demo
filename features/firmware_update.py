import time
import subprocess
import pyautogui
from features.dfu_helper import load_config

pyautogui.FAILSAFE = True

def firmware_update(redacted_exe):
    """
    Run firmware update using a single redacted EXE.
    """
    cfg = load_config()
    dfu_wait = cfg.get("dfu_wait_before_exit_sec", 80)

    print(f"\n Running DFU for EXE: {redacted_exe}")
    proc = subprocess.Popen(
        redacted_exe,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    print(f" Waiting for DFU to complete ({dfu_wait}s)...")
    time.sleep(dfu_wait)

    print(" Sending ESC to close DFU")
    pyautogui.press("esc")
    time.sleep(5)
    proc.terminate()

    print(" Firmware update completed successfully")
    return True