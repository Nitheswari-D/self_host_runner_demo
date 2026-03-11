#Power Cycle
COMMAND_POWER_ON = "on"
COMMAND_POWER_OFF = "off"
DEFAULT_ITERATIONS = 1
DEVICE_ENUM_TIMEOUT_SEC = 60
RECORDING_DURATION = 60
IP_ADDRESS = "192.168.0.100"
DEVICE_INFO_FILE_PATH = r"data\device_data.json"


#LED Enumeration
CAMERA_DEVICE_NAME = "Brio 501"
REFERENCE_IMG_PATH  = r"data\Images\Reference_img.jpg"  
SAVE_DIR = r"data\Images"

#DFU Bins
BIN_PATH_1 = r"data\build\bin_files\BanjoHeadset_1.2_build2586_signed_prod.bin"
BIN_PATH_2 = r"data\build\bin_files\BanjoHeadset_1.2_build2587_signed_prod.bin"

#Double DFU
EXE_PATH_1 = r"data\build\exe_files\1.2_build2586_redacted_build\DFU_ONLY_Centpp_Redacted.exe"
EXE_PATH_2 = r"data\build\exe_files\1.2_build2587_redacted_build\DFU_ONLY_Centpp_Redacted.exe"
UPDATE_CYCLES = 1


DEVICE_NAME = {
    "BANJO":{
        "audio_name":"Logi Zone wired 2 B2B",
        "vid":0x046D, 
        "pid":0xB28, 
        "usage_pg":65299, 
        "state": "U"
    },
    "SONIC":{
        "audio_name":"Logi Zone wireless 2 ES B2B-USB", 
        "vid":0x046D, 
        "pid":0xB26, 
        "usage_pg":65299, 
        "state": "U"
    },
    "MARIO":{
        "audio_name":"Logi Zone wireless pro",
        "vid":0x046D, 
        "pid":0x0B24, 
        "usage_pg":65299, 
        "state": "U",
    }
}
