import pytest
from data.config_data import DEVICE_INFO_FILE_PATH
from features.device_setup import read_device_info, setup_device
from features.power import power_on, power_off
from features.device_enum_esp import device_enumerate

@pytest.fixture(scope="session")
def context():
    context = {}

    info = read_device_info(DEVICE_INFO_FILE_PATH)

    raw_name = info.get("device_name")
    if not raw_name:
        raise ValueError("device_name missing in device_info.json")

    context["build"] = info.get("build_version", "UNKNOWN")

    setup = setup_device(context, raw_name)
    print("setup value :" , setup)

    return context


@pytest.fixture(scope="module")
def redact_setup_module(context):
    power_on(context)
    print("Power on successful")

    device_enumerate(context)
    print("Device Enumerated")

    try:
        yield 

    finally:
        power_off(context)
        print("Power off successful")




