import google.generativeai as genai
import os

def create_caption(scene_description):
    genai.configure(api_key=os.getenv("AIzaSyCNk3szXbjaIAw-3kCDzfFCE7fGWYV6lKs"))
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(
        f"Write a short, engaging Instagram-style caption for a fashionable AI influencer. Scene: {scene_description}. "
        "Make it sound natural, fun, and a bit flirty. Emojis allowed. Keep under 200 characters."
    )
    return response.text.strip()
