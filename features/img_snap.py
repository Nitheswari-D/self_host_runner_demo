import cv2
import time
from pygrabber.dshow_graph import FilterGraph
from datetime import datetime
from features.img_comparision import img_cmp
from data.config_data import REFERENCE_IMG_PATH, SAVE_DIR

def get_webcam_index(device_name):  
    graph = FilterGraph()
    devices = graph.get_input_devices()

    device_name = device_name.lower()

    for index, name in enumerate(devices):
        if device_name in name.lower():
            print(f"Webcam found: {name}")
            return index

    print("Webcam not found")
    return None


def img_snap(CAMERA_DEVICE_NAME): 
    
    index = get_webcam_index(CAMERA_DEVICE_NAME)

    time.sleep(2)
    cap = cv2.VideoCapture(index,cv2.CAP_DSHOW)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 60)

    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    target_focus = 130
    cap.set(cv2.CAP_PROP_FOCUS, target_focus) 
            
    ret, frame = cap.read()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    actual_filepath = f"{SAVE_DIR}/webcam_{timestamp}.jpg"
    cv2.imwrite(actual_filepath,frame)
    print("Snap took successfully")
    
    cap.release()
    cv2.destroyAllWindows()
    
    return img_cmp(REFERENCE_IMG_PATH,actual_filepath)

    print(f"Video saved to: {actual_filepath}")