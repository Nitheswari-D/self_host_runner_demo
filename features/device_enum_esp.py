import time
from data.config_data import DEVICE_ENUM_TIMEOUT_SEC
from features.check_device_enum import check_device

def device_enumerate(context):
    
    print("======Running enumeration test...======")
    device = context["device"]
    device_name = device["name"].lower()
    print("The device name is: ",device_name)

    # start_time = context.get("start_time")
    # if not start_time:
    #     print("ERROR: start_time not found in context")
    #     return False
    
    for _ in range(DEVICE_ENUM_TIMEOUT_SEC):
        if check_device(device_name):
            # enum_time = time.time() - start_time
            # print(f"Device enumerated after Power ON in {enum_time:.2f} seconds")
            return True
        time.sleep(0.5)
    
    print("ERROR: Device enumeration timeout")   
    return False
