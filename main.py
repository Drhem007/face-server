from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Home test route
@app.route("/")
def home():
    return "✅ Face verification server is running!"

# Face verification endpoint
@app.route("/verify_face", methods=["POST"])
def verify_face():
    data = request.get_json()
    image_path = data.get("image_path")  # ESP will send this

    # Example logic: simulate match for student1
    if "student1" in image_path.lower():
        return jsonify({"access": True})
    else:
        return jsonify({"access": False})

# Run the app on 0.0.0.0 and use PORT from environment for Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway sets this
    app.run(host="0.0.0.0", port=port, debug=True)
