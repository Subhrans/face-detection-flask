from flask import Flask, render_template, Response

from utils import generate_frames

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/face-detection")
def face_detection():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace;boundary=frame")


if __name__ == "__main__":
    app.run(port=5001, debug=True)
