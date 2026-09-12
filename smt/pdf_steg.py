from pypdf import PdfReader, PdfWriter
from .crypto import encrypt_data, decrypt_data
import os

def encode_pdf(in_pdf: str, payload: str, password: str, out_pdf: str):
    """Hides encrypted payload in a custom PDF metadata key."""
    if not os.path.exists(in_pdf):
        raise FileNotFoundError(f"Input PDF not found: {in_pdf}")

    encrypted = encrypt_data(payload.encode('utf-8'), password)
    data_to_hide = encrypted + b"<EOF>"
    
    reader = PdfReader(in_pdf)
    writer = PdfWriter()
    
    for page in reader.pages:
        writer.add_page(page)
        
    metadata = reader.metadata
    # pypdf metadata must be a dictionary. Keys must start with a slash (/)
    new_metadata = {}
    if metadata:
        for k, v in metadata.items():
            new_metadata[k] = v
            
    # Convert binary payload to hex string for safe storage in metadata
    new_metadata["/StegoData"] = data_to_hide.hex()
    writer.add_metadata(new_metadata)
    
    with open(out_pdf, "wb") as f:
        writer.write(f)
    print(f"Successfully hid payload in PDF metadata at {out_pdf}")

def decode_pdf(in_pdf: str, password: str) -> str:
    """Extracts and decrypts payload from PDF metadata."""
    if not os.path.exists(in_pdf):
        raise FileNotFoundError(f"Input PDF not found: {in_pdf}")

    reader = PdfReader(in_pdf)
    metadata = reader.metadata
    
    if not metadata or "/StegoData" not in metadata:
        raise ValueError("No steganographic payload (/StegoData) found in the PDF metadata.")
        
    hex_data = metadata["/StegoData"]
    try:
        data_to_hide = bytes.fromhex(hex_data)
    except ValueError as e:
        raise ValueError(f"Failed to decode hex data from metadata: {e}")
    
    if b"<EOF>" not in data_to_hide:
        raise ValueError("No <EOF> delimiter found in the payload.")
        
    encrypted_payload = data_to_hide.split(b"<EOF>")[0]
    
    decrypted = decrypt_data(encrypted_payload, password)
    return decrypted.decode('utf-8')
