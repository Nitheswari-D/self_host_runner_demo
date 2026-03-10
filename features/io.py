from time import sleep

def clear_input_report(device):
    device.get_input_report(7,64)
    sleep(.1)


def write_output_report(device, buff):
    clear_input_report(device)
    device.write(bytes(buff))
    print(f"Sent: {' '.join(f'{int(b):02X}' for b in buff)}")
    
    
def get_in_report(device):
    sleep(2)
    response = device.get_input_report(7, 64)
    # Ensure all bytes are ints (sometimes may be str or other)
    response = [int(b) for b in response]
    print(f"Received: {' '.join(f'{b:02X}' for b in response)}")
    return response