import subprocess
from .crypto import encrypt_data, decrypt_data

ZWSP = '\u200B'
ZWNJ = '\u200C'

def bytes_to_zw(data: bytes) -> str:
    """Converts bytes to a string of zero-width characters."""
    binary_str = "".join(f"{byte:08b}" for byte in data)
    return "".join(ZWSP if bit == '0' else ZWNJ for bit in binary_str)

def zw_to_bytes(zw_str: str) -> bytes:
    """Converts a string of zero-width characters back to bytes."""
    binary_str = "".join('0' if char == ZWSP else '1' for char in zw_str if char in (ZWSP, ZWNJ))
    if not binary_str:
        return b""
    byte_chunks = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    return bytes(int(chunk, 2) for chunk in byte_chunks if len(chunk) == 8)

def encode_git(payload: str, password: str):
    """Encodes an encrypted payload into the latest git commit message using zero-width characters."""
    encrypted = encrypt_data(payload.encode('utf-8'), password)
    data_to_hide = encrypted + b"<EOF>"
    
    zw_payload = bytes_to_zw(data_to_hide)
    
    # Get current commit message
    try:
        current_msg = subprocess.check_output(["git", "log", "-1", "--pretty=%B"]).decode('utf-8')
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Failed to get git commit message. Are you in a git repository with at least one commit?") from e
        
    new_msg = current_msg + zw_payload
    
    # Amend commit
    try:
        subprocess.check_call(["git", "commit", "--amend", "-m", new_msg])
        print("Successfully amended the latest git commit with the hidden payload.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to amend git commit: {e}")

def decode_git(password: str) -> str:
    """Decodes and decrypts a payload from the latest git commit message."""
    try:
        current_msg = subprocess.check_output(["git", "log", "-1", "--pretty=%B"]).decode('utf-8')
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Failed to get git commit message. Are you in a git repository?") from e
        
    # Extract ZW characters
    zw_chars = [c for c in current_msg if c in (ZWSP, ZWNJ)]
    if not zw_chars:
        raise ValueError("No steganographic payload (zero-width characters) found in the latest commit message.")
        
    zw_str = "".join(zw_chars)
    data_to_hide = zw_to_bytes(zw_str)
    
    if b"<EOF>" not in data_to_hide:
        raise ValueError("No <EOF> delimiter found in the payload.")
        
    encrypted_payload = data_to_hide.split(b"<EOF>")[0]
    
    decrypted = decrypt_data(encrypted_payload, password)
    return decrypted.decode('utf-8')
