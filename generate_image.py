import requests
import random

def generate_fashion_images(prompt, seed, width=2048, height=2730):
    """
    Generate a 3:4 portrait that looks like a real phone photo.
    Add a random shot type to the prompt for natural variety.
    """
    # Randomly choose shot type for natural variety
    shot_types = [
        "full body shot, standing, looking at camera",
        "half body shot, from waist up, candid",
        "close-up selfie, face filling the frame, slight smile"
    ]
    shot_type = random.choice(shot_types)

    base_character = (
        f"a beautiful 25-year-old Caucasian woman with long wavy brown hair and green eyes, "
        f"natural makeup, soft skin texture, visible pores, not airbrushed, "
        f"photographed with an iPhone 15 Pro Max, natural window light, "
        f"casual clothing, messy bun, {shot_type}, "
        f"real life, unedited, instagram story style, sharp details"
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
