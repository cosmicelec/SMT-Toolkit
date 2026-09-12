import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def get_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200000,
        backend=default_backend()
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt_data(payload: bytes, password: str) -> bytes:
    """Encrypts data using AES-GCM (Authenticated Encryption)."""
    salt = os.urandom(16)
    nonce = os.urandom(12)  # Recommended nonce length for GCM is 96 bits (12 bytes)
    key = get_key(password, salt)
    
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, payload, None)
    
    # Prepend salt and nonce to the ciphertext
    return salt + nonce + ciphertext

def decrypt_data(encrypted_data: bytes, password: str) -> bytes:
    """Decrypts data using AES-GCM (Authenticated Encryption)."""
    if len(encrypted_data) < 28:
        raise ValueError("Invalid encrypted data format or corrupted data.")
        
    salt = encrypted_data[:16]
    nonce = encrypted_data[16:28]
    ciphertext = encrypted_data[28:]
    
    key = get_key(password, salt)
    aesgcm = AESGCM(key)
    
    try:
        decrypted = aesgcm.decrypt(nonce, ciphertext, None)
        return decrypted
    except Exception as e:
        raise ValueError("Decryption failed. Incorrect password or data tampering detected.") from e
