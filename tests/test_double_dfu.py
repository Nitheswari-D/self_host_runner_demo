import pytest
from features.redact_generator import create_redacted_exe
from features.power import power_on, power_off
from features.device_enum_esp import device_enumerate
from features.firmware_update import firmware_update
from data.config_data import BIN_PATH_1, BIN_PATH_2, EXE_PATH_1, EXE_PATH_2, UPDATE_CYCLES


params = []
ids = []

for cycle in range(UPDATE_CYCLES):
    params.append((cycle, EXE_PATH_1))
    params.append((cycle, EXE_PATH_2))

    ids.append(f"cycle{cycle+1}-FW1")
    ids.append(f"cycle{cycle+1}-FW2")


@pytest.fixture(scope="module")
def doubledfu_setup_module(context):

    assert power_on(context) is True, "Power ON failed"
    assert device_enumerate(context) is True, "Device Enumeration Failed"

    print("Generating EXE from BIN 1")
    create_redacted_exe(BIN_PATH_1)

    print("Generating EXE from BIN 2")
    create_redacted_exe(BIN_PATH_2)

    yield

    assert power_off(context) is True, "Power off failed"


@pytest.mark.usefixtures("doubledfu_setup_module")
@pytest.mark.parametrize("cycle, exe_path", params, ids=ids)
def test_firmware_cycle(cycle, exe_path):

    print(f"\nCycle {cycle+1} → Updating firmware using {exe_path}")

    updated_version = firmware_update(exe_path)

    assert updated_version, f"Cycle {cycle+1} firmware update failed"