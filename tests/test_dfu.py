import pytest
from features.firmware_update import firmware_update
from features.redact_generator import create_redacted_exe
from data.config_data import BIN_PATH_1,EXE_PATH_1

def test_firmware_update(redact_setup_module):

    print("Converting BIN → EXE")
    exe_path = create_redacted_exe(BIN_PATH_1)
    assert exe_path, "EXE generation failed"

    print("Updating Firmware")
    updated_version = firmware_update(EXE_PATH_1)
    assert updated_version, "Firmware update failed"

    # print("=== Validating Version ===")
    # assert updated_version == FW_VERSION, (
    #     f"Version mismatch: expected {FW_VERSION}, got {updated_version}"
    # )

