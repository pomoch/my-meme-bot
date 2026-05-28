import requests

def generate_fashion_images(prompt, seed, width=1440, height=1800):
    """
    Generate ultra‑sharp images with camera‑specific keywords and increased resolution.
    """
    base_character = (
        "a beautiful Caucasian woman with long wavy brown hair, green eyes, "
        "heart-shaped face, natural makeup, fit toned body, 25 years old, "
        "shot on Canon EOS R5, 50mm f/1.4 lens, 8k resolution, ultra HD, "
        "tack sharp focus, detailed skin texture, professional studio lighting, "
        "noise-free, high-end commercial photography"
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
