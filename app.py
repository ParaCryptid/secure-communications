
import os
import logging
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from transformers import pipeline
from logging.handlers import RotatingFileHandler

# ==== Setup Logging ====
LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)
log_handler = RotatingFileHandler(f'{LOG_DIR}/app.log', maxBytes=1000000, backupCount=3)
logging.basicConfig(handlers=[log_handler], level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# ==== Flask App Setup ====
app = Flask(__name__)
socketio = SocketIO(app)

# ==== AI Model for Message Analysis ====
message_analyzer = pipeline("sentiment-analysis")

# ==== Encryption Key Setup ====
private_key = x25519.X25519PrivateKey.generate()
public_key = private_key.public_key()

def derive_shared_key(peer_public_bytes):
    peer_public_key = x25519.X25519PublicKey.from_public_bytes(peer_public_bytes)
    shared_secret = private_key.exchange(peer_public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'secure-communications',
    ).derive(shared_secret)
    return derived_key

def encrypt_message(message, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    return iv + ciphertext

def decrypt_message(ciphertext, key):
    iv = ciphertext[:16]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext[16:]) + decryptor.finalize()
    return plaintext.decode()

# ==== Flask Routes ====
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    message = data.get("message", "")
    logger.info(f"Analyzing message: {message}")
    result = message_analyzer(message)
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "mode": "offline" if os.getenv("OFFLINE_MODE") == "1" else "online"})

# ==== Socket Events ====
@socketio.on('connect')
def handle_connect():
    logger.info("Client connected via WebSocket")
    emit('server_response', {'data': 'Connected to secure server'})

@socketio.on('secure_message')
def handle_secure_message(data):
    try:
        logger.info("Received secure message via socket")
        message = data.get("message", "")
        peer_key = bytes.fromhex(data.get("public_key", ""))
        shared_key = derive_shared_key(peer_key)
        encrypted = encrypt_message(message, shared_key)
        emit('server_response', {'data': encrypted.hex()})
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        emit('server_response', {'error': 'Encryption failed'})

# ==== Main Entrypoint ====
if __name__ == '__main__':
    offline_mode = os.getenv("OFFLINE_MODE") == "1"
    logger.info(f"Starting app (OFFLINE_MODE={offline_mode})")
    socketio.run(app, host='0.0.0.0', port=8080)
