from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from ocr_engine import extract_plate_text
from models import find_owner_by_plate, create_owner_vehicle
from notification_service import send_email, send_sms

app=Flask(__name__); CORS(app)
UPLOAD_FOLDER="uploads"; os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def idx():
    return jsonify({"status":"ok"}),200

@app.post("/api/lookup_plate")
def lookup():
    if "image" not in request.files:
        return jsonify({"error":"no image"}),400
    f=request.files["image"]
    path=os.path.join(UPLOAD_FOLDER,f.filename)
    f.save(path)
    text,conf=extract_plate_text(path)
    if not text:
        return jsonify({"error":"no plate","ocr_confidence":conf}),404
    owner=find_owner_by_plate(text)
    return jsonify({"plate":text,"ocr_confidence":conf,"owner":owner}),200

@app.post("/api/register_owner_vehicle")
def reg():
    d=request.json
    req=["name","plate","year"]
    if any(k not in d for k in req):
        return jsonify({"success":False,"error":"missing fields"}),400
    created=create_owner_vehicle(d["name"],d.get("phone",""),d.get("email",""),d["plate"],d.get("brand",""),d.get("model",""),int(d["year"]))
    return jsonify({"success":True,"data":created}),201

@app.post("/api/notify_owner")
def notify():
    d=request.json
    plate=d.get("plate"); ch=d.get("channel"); msg=d.get("message","")
    owner=find_owner_by_plate(plate)
    if not owner: return jsonify({"success":False,"error":"no owner"}),404
    if ch=="email": ok=send_email(owner["owner_email"],"Notificación",msg)
    else: ok=send_sms(owner["owner_phone"],msg)
    return jsonify({"success":ok}),200

if __name__=="__main__":
    app.run()
