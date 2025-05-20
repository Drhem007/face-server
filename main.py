from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Face Recognition Server is Running!"

@app.route("/verify_face", methods=["POST"])
def verify_face():
    data = request.get_json()
    image_path = data.get("image_path")

    # Simulate image recognition
    if image_path == "student1.jpg":
        return jsonify({ "access": True })
    else:
        return jsonify({ "access": False })

if __name__ == "__main__":
    app.run(debug=True)
