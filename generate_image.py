import requests

def generate_fashion_images(prompt, seed, width=2048, height=2048):
    """
    Generate an image that looks like it was taken with a phone –
    casual, realistic, no studio perfection.
    """
    base_character = (
        "a candid iPhone 15 Pro Max selfie of a beautiful 25-year-old Caucasian woman, "
        "long wavy brown hair, green eyes, natural makeup, soft smile, "
        "natural window light, slight skin texture, visible pores, not airbrushed, "
        "casual clothing, messy bun, phone camera quality, slight motion blur, "
        "real life, unedited, instagram story style, 2025"
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
