from flask import Flask, jsonify
from routes.auth import auth_bp
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(auth_bp)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "Auth Service is running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)