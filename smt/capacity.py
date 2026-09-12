import os
import wave
from PIL import Image

def get_capacity_report(file_path: str) -> str:
    """Calculates safe steganographic limits based on file type."""
    if not os.path.exists(file_path):
        return f"Error: File not found: {file_path}"
    
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif']:
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                capacity = (width * height * 3) // 8
                return f"Image Capacity for {os.path.basename(file_path)}: {capacity} bytes"
        except Exception as e:
            return f"Error reading image: {e}"
            
    elif ext in ['.wav']:
        try:
            with wave.open(file_path, 'rb') as audio:
                frames = audio.getnframes()
                capacity = frames // 8
                return f"Audio Capacity for {os.path.basename(file_path)}: {capacity} bytes"
        except Exception as e:
            return f"Error reading audio: {e}"
            
    elif ext in ['.txt', '.pdf']:
        return f"Capacity for {os.path.basename(file_path)}: Unlimited (increases file size)"
        
    else:
        return f"Capacity for {os.path.basename(file_path)}: Unlimited (increases file size)"
