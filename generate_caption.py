from google import genai
import os

def create_caption(scene_description):
    """Generate a short Instagram‑style caption using Gemini (official google‑genai SDK)."""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.5-flash",  # free, fast, good enough for captions
        contents=(
            f"Write a short, engaging Instagram-style caption for a fashionable AI influencer. "
            f"Scene: {scene_description}. "
            f"Make it sound natural, fun, and a bit flirty. Emojis allowed. Keep under 200 characters."
        ),
    )
    return response.text.strip()
