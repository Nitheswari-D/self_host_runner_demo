from features.send_esp_cmd import send_command_to_device
from data.config_data import IP_ADDRESS, COMMAND_POWER_ON, COMMAND_POWER_OFF


def power_on(context):
    print("======== Running POWER ON ========")

    device = context["device"]
    state = device["state"]

    if not send_command_to_device(IP_ADDRESS, state):
        print("false - state not sent properly!")
        return False

    if not send_command_to_device(IP_ADDRESS, COMMAND_POWER_ON):
        return False

    return True


def power_off(context):
    print("======== Running POWER OFF ========")

    if not send_command_to_device(IP_ADDRESS, COMMAND_POWER_OFF):
        return False

    return True