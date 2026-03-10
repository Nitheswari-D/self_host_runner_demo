import json
import pytest
from datetime import datetime
from features.device_enumeration import find_dut, open_device
from features.io import write_output_report, get_in_report
from features.byte_comparison import bytes_comparison
from features.generate_report import generate_html_report
from features.power import power_on, power_off
from features.device_enum_esp import device_enumerate
from features.config_loader import DEVICE_NAME_LOWER


RESULTS = []

with open(f"data/tde_data/{DEVICE_NAME_LOWER}.json", "r") as f:
    data = json.load(f)


@pytest.fixture(scope="module")
def device_enum(context):
    assert power_on(context) is True, "Power ON failed"
    assert device_enumerate(context) is True, "Device Enumeration Failed"
    device = open_device()

    yield device

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"tde_report_{timestamp}.html"
    generate_html_report(RESULTS, filename)
    device.close()
    power_off(context)
    print("power off success")

    

@pytest.mark.parametrize(
    "label,command_set",
    data.items()
)
def test_tde_command(device_enum, label, command_set):        
    command = command_set["command"]
    expected = command_set["expected_response"]

    write_output_report(device_enum, command)
    response = get_in_report(device_enum)

    start_idx = bytes_comparison(expected, response)
    passed = start_idx != -1

    RESULTS.append({
        "label": label,
        "command": command,
        "expected_hex": [f"{b:02X}" for b in expected],
        "received_hex": [f"{b:02X}" for b in response],
        "start_idx": start_idx,
        "passed": passed
    })
    assert passed, f"{label} FAILED"
