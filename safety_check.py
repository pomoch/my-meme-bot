import opennsfw2 as n2
from PIL import Image

def is_safe(image_path, threshold=0.5):
    """Return True if image is SFW (NSFW probability < threshold)."""
    pil_image = Image.open(image_path)
    nsfw_prob = n2.predict_image(pil_image)
    print(f"NSFW probability for {image_path}: {nsfw_prob}")
    return nsfw_prob < threshold
