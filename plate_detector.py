import cv2

def detect_plate_region(img):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return gray
