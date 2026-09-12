import qrcode
import base64
import cv2
from .crypto import encrypt_data, decrypt_data

def encode_qr(target_url: str, payload: str, password: str, out_path: str):
    """Embeds encrypted payload into a target URL and generates a QR code."""
    encrypted = encrypt_data(payload.encode('utf-8'), password)
    data_to_hide = encrypted + b"<EOF>"
    encoded_b64 = base64.urlsafe_b64encode(data_to_hide).decode('utf-8')
    
    full_url = f"{target_url}#{encoded_b64}"
    
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(full_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(out_path)
    print(f"Successfully generated QR code with embedded payload at {out_path}")

def decode_qr(img_path: str, password: str) -> str:
    """Extracts and decrypts payload from a QR code."""
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Could not read image at {img_path}")
        
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    
    if not data:
        raise ValueError("Could not detect or decode QR code from the image.")
        
    if '#' not in data:
        raise ValueError("No steganographic payload found in the QR code (missing '#' separator).")
        
    target_url, encoded_b64 = data.rsplit('#', 1)
    try:
        data_to_hide = base64.urlsafe_b64decode(encoded_b64)
    except Exception as e:
        raise ValueError(f"Failed to decode base64 payload: {e}")
        
    if b"<EOF>" not in data_to_hide:
        raise ValueError("No <EOF> delimiter found in the payload.")
        
    encrypted_payload = data_to_hide.split(b"<EOF>")[0]
    
    decrypted = decrypt_data(encrypted_payload, password)
    return decrypted.decode('utf-8')
