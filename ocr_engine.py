import cv2, pytesseract
from pytesseract import Output
from plate_detector import detect_plate_region

def preprocess_for_tesseract(img):
    h,w = img.shape[:2]
    scale = 300 / max(h,w)
    if scale<1.0:
        img = cv2.resize(img, None, fx=scale, fy=scale)
    blur=cv2.GaussianBlur(img,(3,3),0)
    _,th=cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return th

def extract_plate_text(path):
    img=cv2.imread(path)
    if img is None: return None,0.0
    region=detect_plate_region(img)
    if region is None:
        region=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    th=preprocess_for_tesseract(region)
    cfg="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    data=pytesseract.image_to_data(th, output_type=Output.DICT, config=cfg)
    texts=[]; confs=[]
    for t,c in zip(data["text"], data["conf"]):
        t=t.strip()
        try: cv=float(c)
        except: cv=-1
        if t and cv>=0:
            texts.append(t); confs.append(cv)
    if not texts: return None,0.0
    best="".join(texts).replace(" ","").upper()
    avg=sum(confs)/len(confs) if confs else 0
    return best, avg/100.0
