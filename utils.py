import cv2
from flask import abort


def generate_frames():
    camera = cv2.VideoCapture(0)

    while True:
        state, frame = camera.read()
        if not state:
            return abort(404, "we unable to read web cam")
        detector = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
        eye_cascade = cv2.CascadeClassifier("haarcascade/haarcascade_eye.xml")
        faces= detector.detectMultiScale(frame,1.1,7)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        for x,y,w,h in faces:
            cv2.rectangle(frame, (x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh),(0,255,0), 2)

        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
