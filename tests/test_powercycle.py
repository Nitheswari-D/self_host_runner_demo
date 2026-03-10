from features.power import power_on, power_off
from features.device_enum_esp import device_enumerate
from features.img_snap import img_snap
from data.config_data import CAMERA_DEVICE_NAME
import pytest


@pytest.mark.dependency(name="power_on")
def test_power_on(context):
    assert power_on(context) is True, "Power ON failed"


# @pytest.mark.dependency(name="led_enum", depends=["power_on"])
# def test_led_enumeration(context):
#     assert img_snap(CAMERA_DEVICE_NAME) is True, "LED Enumeration failed"


@pytest.mark.dependency(name="device_enum", depends=["power_on"])
def test_device_enumeration(context):
    assert device_enumerate(context) is True, "Device enumeration failed"


@pytest.mark.dependency(depends=["device_enum"])
def test_power_off(context):
    assert power_off(context) is True, "Power OFF failed"
