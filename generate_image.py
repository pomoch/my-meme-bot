import requests

def generate_fashion_images(prompt, seed, width=2048, height=2048):
    base = (
        "a beautiful Caucasian woman with long wavy brown hair, green eyes, "
        "heart-shaped face, natural makeup, fit toned body, 25 years old, "
        "shot on Hasselblad X2D 100C, 100 megapixel, f/1.4, tack-sharp focus, "
        "ultra high definition, professional lighting, skin texture visible, "
        "noise-free, editorial fashion photography, 2026 standards"
    )
    full_prompt = f"{base}, {prompt}"
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
