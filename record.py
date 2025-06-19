from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("record.html")

@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"message": "No video uploaded"}), 400

    video = request.files["video"]
    video_filename = f"video_{len(os.listdir(UPLOAD_FOLDER)) + 1}.webm"
    video_path = os.path.join(UPLOAD_FOLDER, video_filename)
    video.save(video_path)

    return jsonify({"message": "Video uploaded successfully!", "file_path": f"/uploads/{video_filename}"})

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
