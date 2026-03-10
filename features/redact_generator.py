import os
import subprocess
import pyautogui

from features.dfu_helper import load_config, wait, extract_fw_version, get_build_output_dir, wait_for_redacted_exe, select_usb_product


def create_redacted_exe(bin_path):
    """
    Create a single redacted EXE from the DFU file.
    Returns path of the created EXE.
    """
    cfg = load_config()
    
    if not bin_path: 
        raise ValueError("DFU bin path is required")
        
    dfu_bin = bin_path

    print("Using DFU bin:", dfu_bin)

    if not os.path.exists(dfu_bin):
        raise RuntimeError(f"DFU BIN not found: {dfu_bin}")

    centpp = cfg["centpp_exe"]
    output_dir = cfg.get("output_dir", os.path.expanduser("~"))

    build_output_dir = get_build_output_dir(output_dir, dfu_bin)

    # Launch CentPP
    centpp_proc = subprocess.Popen(
        centpp,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    wait(4)
    pyautogui.press("r")
    wait(2)
    pyautogui.press("enter")
    wait(3)

    pyautogui.write(build_output_dir, interval=0.02)
    pyautogui.press("enter")
    wait(3)

    if cfg.get("dfu_only", True):
        pyautogui.press("enter")
        wait(2)

    pyautogui.write(dfu_bin, interval=0.02)
    pyautogui.press("enter")
    wait(2)

    fw_version = extract_fw_version(dfu_bin)
    pyautogui.write(fw_version, interval=0.02)
    pyautogui.press("enter")

    if not select_usb_product(cfg):
        centpp_proc.terminate()
        raise RuntimeError("USB product selection failed")

    # Wait for EXE
    redacted_exe = wait_for_redacted_exe(build_output_dir, cfg.get("usb_select_timeout_sec", 60))
    centpp_proc.terminate()

    if not redacted_exe:
        raise RuntimeError("Redacted EXE not created")

    print(" Redacted EXE created:", redacted_exe)
    return redacted_exe