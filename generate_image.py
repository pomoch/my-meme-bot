import requests

def generate_fashion_images(prompt, seed, width=2048, height=2048):
    """
    Ask Pollinations for the sharpest possible image.
    We upscale later, but the base must be incredibly detailed.
    """
    base_character = (
        "a beautiful Caucasian woman with long wavy brown hair, green eyes, "
        "heart-shaped face, natural makeup, fit toned body, 25 years old, "
        "photographed with a Hasselblad H6D-100c, 100 megapixels, f/1.4, "
        "tack‑sharp focus, ultra high definition, intricate skin texture, "
        "every eyelash visible, professional studio lighting, noise‑free, "
        "hyper‑realistic, vibrant colors, editorial fashion photography, 2026 aesthetic"
    )
    full_prompt = f"{base_character}, {prompt}"
    encoded = requests.utils.quote(full_prompt)
    url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?model=flux"
        f"&width={width}"
        f"&height={height}"
        f"&seed={seed}"
        f"&nologo=true"
    )
    return url
