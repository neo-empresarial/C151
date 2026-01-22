from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

KEY_FILE = "secret.key"

def load_key():
    env_key = os.getenv("SECRET_KEY")
    if env_key:
        try:
            return env_key.encode() if isinstance(env_key, str) else env_key
        except Exception as e:
            print(f"Error loading key from env: {e}")
    
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    print("WARNING: No SECRET_KEY found. Generating a new one locally.")
    return generate_key()

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key

try:
    key = load_key()
    cipher_suite = Fernet(key)
except Exception as e:
    print(f"CRITICAL SECURITY ERROR: Could not initialize encryption: {e}")
    cipher_suite = Fernet(Fernet.generate_key())

def encrypt_data(data: str) -> str:
    if not data:
        return ""
    try:
        encrypted_bytes = cipher_suite.encrypt(data.encode())
        return encrypted_bytes.decode()
    except Exception as e:
        print(f"Encryption error: {e}")
        return ""

def decrypt_data(data: str) -> str:
    if not data:
        return ""
    try:
        decrypted_bytes = cipher_suite.decrypt(data.encode())
        return decrypted_bytes.decode()
    except Exception as e:
        return ""

def encrypt_bytes(data: bytes) -> bytes:
    if not data:
        return b""
    try:
        return cipher_suite.encrypt(data)
    except Exception as e:
        print(f"Encryption error: {e}")
        return b""

def decrypt_bytes(data: bytes) -> bytes:
    if not data:
        return b""
    try:
        return cipher_suite.decrypt(data)
    except Exception as e:
        return b""
