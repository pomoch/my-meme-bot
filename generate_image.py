import requests

def generate_fashion_images(prompt, seed, width=1080, height=1350):
    """
    High-quality image with consistent character using fixed seed.
    Adds camera-specific keywords for realism and sharpness.
    """
    base_character = (
        "a beautiful Caucasian woman with long wavy brown hair, green eyes, "
        "heart-shaped face, natural makeup, fit toned body, 25 years old, "
        "shot on iPhone 15 Pro Max, 4k, cinematic, ultra sharp details, "
        "professional lighting, natural skin texture, highly detailed"
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
