import requests
import random

def generate_fashion_images(prompt, seed, width=2048, height=2730):
    """
    Use flux-realism model + negative prompt for photorealistic results.
    Random shot type (full/half/close-up) for natural variety.
    """
    shot_types = [
        "full body shot, standing, looking at camera",
        "half body shot, from waist up, candid",
        "close-up selfie, face filling the frame, slight smile"
    ]
    shot_type = random.choice(shot_types)

    base_character = (
        f"a beautiful 25-year-old Caucasian woman with long wavy brown hair and green eyes, "
        f"natural skin texture, visible pores, minor imperfections, not airbrushed, "
        f"{shot_type}, "
        f"shot on iPhone 15 Pro Max, natural window light, 24mm lens, f/1.8, "
        f"raw unprocessed photo, candid moment, real life, 2025"
    )
    full_prompt = f"{base_character}, {prompt}"

    # Negative prompt – avoids plastic skin, distortions
    negative = "ugly, deformed, blurry, low quality, watermark, text, disfigured, bad anatomy, airbrushed, doll, plastic skin, mutated hands"

    encoded_prompt = requests.utils.quote(full_prompt)
    encoded_negative = requests.utils.quote(negative)

    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?model=flux-realism"
        f"&negative={encoded_negative}"
        f"&width={width}"
        f"&height={height}"
        f"&seed={seed}"
        f"&nologo=true"
    )
    return url
