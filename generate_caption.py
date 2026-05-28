import requests

def create_caption(context):
    prompt = (
        f"Write a short, engaging Instagram-style caption for a fashionable AI influencer. "
        f"Context: {context}. "
        f"Make it sound natural, fun, and a bit flirty. Emojis allowed. Keep under 200 characters."
    )
    encoded = requests.utils.quote(prompt)
    url = f"https://text.pollinations.ai/{encoded}"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200 and resp.text.strip():
            return resp.text.strip()
        else:
            raise ValueError("Empty response")
    except Exception as e:
        print(f"⚠️ Caption generation failed: {e}")
        # Fallback caption
        return "Living my best life, one outfit at a time ✨"
