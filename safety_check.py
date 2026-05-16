import opennsfw2 as n2
from PIL import Image

def is_safe(image_path, threshold=0.5):
    """Return True if image is SFW (probability > threshold)."""
    pil_image = Image.open(image_path)
    # opennsfw2 gives a probability of NSFW (0.0 - 1.0)
    nsfw_prob = n2.predict_image(pil_image)
    print(f"NSFW probability for {image_path}: {nsfw_prob}")
    return nsfw_prob < threshold   # below threshold = safe
