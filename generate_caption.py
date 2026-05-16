import requests

def create_caption(scene_description):
    """Generate a short Instagram-style caption using Pollinations text API (free, no key)."""
    prompt = (
        f"Write a short, engaging Instagram-style caption for a fashionable AI influencer. "
        f"Scene: {scene_description}. "
        f"Make it sound natural, fun, and a bit flirty. Emojis allowed. Keep under 200 characters."
    )
    encoded = requests.utils.quote(prompt)
    url = f"https://text.pollinations.ai/{encoded}"

    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            return resp.text.strip()
        else:
            # Fallback if Pollinations fails
            return "New outfit, who dis? ✨"
    except Exception:
        return "New outfit, who dis? ✨"
