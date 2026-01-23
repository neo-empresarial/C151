from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

from dotenv import set_key

KEY_FILE = "secret.key"
ENV_FILE = ".env"

def is_key_configured():
    """Check if SECRET_KEY is set in environment (not auto-generated)."""
    return os.getenv("SECRET_KEY") is not None

def save_secret_key(key_str: str):
    """Save SECRET_KEY to .env file and reload cipher."""
    try:
        # Validate key format first
        new_key = key_str.encode() if isinstance(key_str, str) else key_str
        try:
            Fernet(new_key)
        except Exception as e:
            print(f"Invalid Fernet key: {e}")
            return False

        # Update current env
        os.environ["SECRET_KEY"] = key_str
        
        # Write to .env file
        # If .env doesn't exist, create it
        if not os.path.exists(ENV_FILE):
            with open(ENV_FILE, 'w') as f:
                f.write("")
        
        set_key(ENV_FILE, "SECRET_KEY", key_str)
        
        # Reload cipher with new key
        global cipher_suite
        cipher_suite = Fernet(new_key)
        return True
    except Exception as e:
        print(f"Error saving SECRET_KEY: {e}")
        return False

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
    # Fallback to avoid crash, but application should ideally block
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
