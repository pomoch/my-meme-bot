import requests
import random

def generate_fashion_images(prompt, seed, width=2048, height=2730):
    """
    Generate photorealistic images using 'photon' model + negative prompt.
    Random shot types for variety.
    """
    shot_types = [
        "full body shot, standing, relaxed pose, natural lighting",
        "half body shot, from waist up, candid, slight movement",
        "close-up selfie, face filling the frame, soft smile, direct eye contact"
    ]
    shot_type = random.choice(shot_types)

    base_character = (
        f"a 25-year-old Caucasian woman with long wavy brown hair, green eyes, "
        f"natural skin texture, visible pores, tiny freckles, not airbrushed, "
        f"{shot_type}, "
        f"shot on iPhone 15 Pro Max, natural daylight, 24mm lens, f/1.8, "
        f"unedited raw photo, instagram story, 2025, casual clothing"
    )
    full_prompt = f"{base_character}, {prompt}"

    # Strong negative prompt – eliminates all AI artifacts
    negative = (
        "cartoon, painting, 3d render, plastic skin, waxy face, airbrushed, doll, "
        "blurred, low quality, bad anatomy, extra fingers, mutated hands, disfigured, "
        "ugly, watermark, text, logo, black and white"
    )
    encoded_prompt = requests.utils.quote(full_prompt)
    encoded_negative = requests.utils.quote(negative)

    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?model=photon"
        f"&negative={encoded_negative}"
        f"&width={width}"
        f"&height={height}"
        f"&seed={seed}"
        f"&nologo=true"
    )
    return url
