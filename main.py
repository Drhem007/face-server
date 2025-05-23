from flask import Flask, request, jsonify
import face_recognition
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load known face encodings from the "known_faces" folder.
known_faces = []
known_names = []

# Ensure the known_faces directory exists
if not os.path.exists("known_faces"):
    os.makedirs("known_faces")

# Loop through all jpg/png files in the directory and load them.
for filename in os.listdir("known_faces"):
    if filename.lower().endswith((".jpg", ".png")):
        path = os.path.join("known_faces", filename)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_faces.append(encodings[0])
            # Store the name (filename without extension) in uppercase.
            known_names.append(os.path.splitext(filename)[0].upper())

@app.route("/check-face", methods=["POST"])
def check_face():
    # Check if a file part is included in the request.
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Secure the filename and save it temporarily.
    filename = secure_filename(file.filename)
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    file_path = os.path.join(temp_dir, filename)
    file.save(file_path)

    # Load the uploaded image and try to detect a face.
    image = face_recognition.load_image_file(file_path)
    uploaded_encodings = face_recognition.face_encodings(image)
    if not uploaded_encodings:
        return jsonify({"access": False, "message": "No face detected"}), 200

    uploaded_encoding = uploaded_encodings[0]
    matches = face_recognition.compare_faces(known_faces, uploaded_encoding)

    if True in matches:
        index = matches.index(True)
        return jsonify({"access": True, "name": known_names[index]}), 200
    else:
        return jsonify({"access": False, "message": "Face not recognized"}), 200

if __name__ == "__main__":
    # Listen on all interfaces and on port 8000.
    app.run(host="0.0.0.0", port=5000)
