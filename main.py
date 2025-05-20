from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def recognize():
    # Ignore incoming data for now and always respond recognized = true
    return jsonify({"recognized": True})

if __name__ == '__main__':
    # Use 0.0.0.0 and port 8080 so Railway can access your app
    app.run(host='0.0.0.0', port=8080)
