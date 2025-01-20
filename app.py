
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from transformers import pipeline
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize AI models (e.g., NLP for message analysis)
message_analyzer = pipeline("sentiment-analysis")

# Initialize encryption keys
private_key = x25519.X25519PrivateKey.generate()
public_key = private_key.public_key()

@app.route('/')
def home():
    return jsonify({
        "message": "Secure Communications repository is fully functional.",
        "features": [
            "Secure Messaging",
            "Real-Time Communication",
            "AI-Powered Analysis"
        ]
    })

@app.route('/analyze_message', methods=['POST'])
def analyze_message():
    data = request.json.get("message", "")
    if not data:
        return jsonify({"error": "No message provided"}), 400
    analysis = message_analyzer(data)
    return jsonify({"analysis": analysis})

@app.route('/secure_message', methods=['POST'])
def secure_message():
    peer_public_key_bytes = request.json.get("peer_public_key", "").encode()
    message = request.json.get("message", "").encode()
    if not peer_public_key_bytes or not message:
        return jsonify({"error": "Invalid input data"}), 400

    peer_public_key = x25519.X25519PublicKey.from_public_bytes(peer_public_key_bytes)
    shared_key = private_key.exchange(peer_public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"secure messaging"
    ).derive(shared_key)

    # Encrypt the message
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(message) + encryptor.finalize()

    return jsonify({"encrypted_message": encrypted_message.hex(), "iv": iv.hex()})

@socketio.on('send_message')
def handle_message(data):
    emit("receive_message", data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5003)
