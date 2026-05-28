import requests

def generate_fashion_images(prompt, seed, width=2048, height=2048):
    base_character = (
        "a beautiful Caucasian woman with long wavy brown hair, green eyes, "
        "heart-shaped face, natural makeup, fit toned body, 25 years old, "
        "photographed with a Phase One IQ4 150MP, f/1.4, extreme sharpness, "
        "every pore visible, hyper‑realistic, 8K texture, professional lighting, "
        "noise‑free, vibrant colors, editorial fashion, 2026 aesthetic"
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
