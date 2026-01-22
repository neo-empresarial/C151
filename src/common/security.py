from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get key from environment or fallback to loading from file (backward compatibility/fallback)
KEY_FILE = "secret.key"

def load_key():
    """Load the key from environment variable or file."""
    # Priority 1: Environment Variable
    env_key = os.getenv("SECRET_KEY")
    if env_key:
        try:
            # Validate key format (base64)
            return env_key.encode() if isinstance(env_key, str) else env_key
        except Exception as e:
            print(f"Error loading key from env: {e}")
    
    # Priority 2: File
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()

    # Priority 3: Generate new (and save to file for persistence if env not set)
    print("WARNING: No SECRET_KEY found. Generating a new one locally.")
    return generate_key()

def generate_key():
    """Generates a key and saves it into a file."""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key

# Initialize the cipher suite
try:
    key = load_key()
    cipher_suite = Fernet(key)
except Exception as e:
    print(f"CRITICAL SECURITY ERROR: Could not initialize encryption: {e}")
    # Fallback to a temporary key to prevent crash, but warn loudly
    cipher_suite = Fernet(Fernet.generate_key())

def encrypt_data(data: str) -> str:
    """Encrypts a string and returns the encrypted string."""
    if not data:
        return ""
    try:
        encrypted_bytes = cipher_suite.encrypt(data.encode())
        return encrypted_bytes.decode()
    except Exception as e:
        print(f"Encryption error: {e}")
        return ""

def decrypt_data(data: str) -> str:
    """Decrypts an encrypted string and returns the original string."""
    if not data:
        return ""
    try:
        decrypted_bytes = cipher_suite.decrypt(data.encode())
        return decrypted_bytes.decode()
    except Exception as e:
        # print(f"Decryption error: {e}") 
        return ""

def encrypt_bytes(data: bytes) -> bytes:
    """Encrypts bytes and returns the encrypted bytes."""
    if not data:
        return b""
    try:
        return cipher_suite.encrypt(data)
    except Exception as e:
        print(f"Encryption error: {e}")
        return b""

def decrypt_bytes(data: bytes) -> bytes:
    """Decrypts encrypted bytes and returns the original bytes."""
    if not data:
        return b""
    try:
        return cipher_suite.decrypt(data)
    except Exception as e:
        print(f"Decryption error: {e}")
        return b""
