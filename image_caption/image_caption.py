"""
Image Captioning Logic
"""

import requests
import base64
from io import BytesIO
from PIL import Image

OLLAMA_API_URL = "http://localhost:11434/api/generate"


def resize_image(image_path, scale=0.5):
    """Resize image by a scale factor and return bytes."""
    with Image.open(image_path) as img:
        new_size = (int(img.width * scale), int(img.height * scale))
        resized_img = img.resize(new_size, Image.LANCZOS)
        print(f"[INFO] Resized image to {new_size[0]}x{new_size[1]}")
        
        buffer = BytesIO()
        resized_img.save(buffer, format="PNG")
        return buffer.getvalue()


def generate_caption(image_path, detail_level='detailed'):
    """Generate a caption from an image."""
    resized_image_bytes = resize_image(image_path)
    img_base64 = base64.b64encode(resized_image_bytes).decode('utf-8')

    prompt = _build_prompt(detail_level)

    payload = {
        "model": "qwen2.5vl:7b",
        "prompt": prompt,
        "images": [img_base64],
        "stream": False
    }

    print(f"[INFO] Sending image for {detail_level} captioning...")
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()

    return response.json().get("response", "").strip()


def _build_prompt(detail_level):
    """Build prompt based on detail level."""
    if detail_level == 'detailed':
        return (
            "Describe the contents of this image in detail. Analyze the objects carefully "
            "and figure out who each character is. Pay attention to the surroundings and "
            "notice all the fine details."
        )
    else:
        return (
            "Briefly describe the main subject of this image in 2-3 concise sentences. "
            "Focus on the key objects or characters only."
        )
