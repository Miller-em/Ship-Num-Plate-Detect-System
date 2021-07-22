import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))

import infer.predict_system as predict_system
import infer.utility as utility
import numpy as np
import cv2
import requests
import base64
import threading

data = {} #data to flask server 
url = "http://ip/xxx"

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


class inferThread(threading.Thread):
    def __init__(self, predict_system):
        threading.Thread.__init__(self)
        self.predict_system = predict_system
    def infer(self , frame):
        flag = False
        rec_res, draw_img, elapse = self.predict_system.main(utility.parse_args(), frame)  #推理
        c_string = ""
        for rec in rec_res:
            flag = True
            dete_object = rec[0]
            c_string += dete_object + '\n' #保存检测信息
        if flag:
            try:
                print(c_string)
                base64_str = cv2.imencode('.jpg', draw_img)[1].tostring()
                data['image_str'] = base64.encodebytes(base64_str).decode("utf-8")
                data['info'] = c_string
                result = requests.request("POST", url, json=data)
                print("检测到文字，send successful!")
            except:
                print(c_string)
                print("检测到文字，send failed!")
        else:
            print("未检测到文字")
        return draw_img, elapse


if __name__ == "__main__":
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    try:
        thread1 = inferThread(predict_system)
        thread1.start()
        thread1.join()
        i = 0
        while 1:
            _,frame = cap.read()
            i += 1
            if (i == 50):
                i = 0
                img,t=thread1.infer(frame)
                print('time->{:.2f}ms'.format(t * 1000))
                #cv2.imshow("result", img)
                if cv2.waitKey(1) & 0XFF == ord('q'):  # 1 millisecond
                    break
    finally:
        # destroy the instance
        cap.release()
        cv2.destroyAllWindows()
