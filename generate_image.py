import requests
import random

def generate_fashion_images(prompt, seed, width=2048, height=2730):
    """
    Ultra‑realistic photo using 'photon' model + negative prompts.
    Random shot type for variety.
    """
    shot_types = [
        "full body shot, standing, looking at camera, casual pose",
        "half body shot, from waist up, candid, slight smile",
        "close-up selfie, face filling the frame, soft expression, eye contact"
    ]
    shot_type = random.choice(shot_types)

    base_character = (
        f"a 25‑year‑old Caucasian woman, long wavy brown hair, green eyes, "
        f"natural skin texture, visible pores, small freckles, not airbrushed, "
        f"{shot_type}, "
        f"shot on iPhone 15 Pro Max, natural daylight, 24mm lens, f/1.8, "
        f"unedited raw photo, instagram story, 2025, casual clothing"
    )
    full_prompt = f"{base_character}, {prompt}"

    # Strong negative prompt to remove all AI artifacts
    negative = (
        "cartoon, painting, illustration, 3d render, plastic skin, waxy face, "
        "airbrushed, doll, blurred, low quality, bad anatomy, extra fingers, "
        "mutated hands, disfigured, ugly, watermark, text, logo, b&w"
    )
    encoded_prompt = requests.utils.quote(full_prompt)
    encoded_negative = requests.utils.quote(negative)

    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?model=photon"                # Photon excels at realistic skin
        f"&negative={encoded_negative}"
        f"&width={width}"
        f"&height={height}"
        f"&seed={seed}"
        f"&nologo=true"
    )
    return url
