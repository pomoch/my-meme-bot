import requests

def create_caption(context):
    """Generate an engaging caption based on today's theme context."""
    prompt = (
        f"Write a short, engaging Instagram-style caption for a fashionable AI influencer. "
        f"Context: {context}. "
        f"Make it sound natural, fun, and a bit flirty. Emojis allowed. Keep under 200 characters."
    )
    encoded = requests.utils.quote(prompt)
    url = f"https://text.pollinations.ai/{encoded}"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            return resp.text.strip()
        else:
            return "New day, new vibes ✨"
    except Exception:
        return "New day, new vibes ✨"
