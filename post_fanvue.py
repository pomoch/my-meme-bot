import requests
import os

def post_to_fanvue(caption, image_b64, video_b64=None):
    """
    Post to Fanvue using their Creator API.
    You must obtain your API key from Fanvue settings -> Developer.
    """
    api_key = os.getenv("FANVUE_API_KEY")
    if not api_key:
        raise Exception("FANVUE_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Build the post payload (adjust fields according to actual Fanvue API docs)
    payload = {
        "post_type": "photo",  # or "video" if video_b64 provided
        "description": caption,
        "tags": ["fashion", "outfit", "ootd"],
        "media": [
            {"type": "image", "data": image_b64}
        ]
    }
    if video_b64:
        payload["media"].append({"type": "video", "data": video_b64})

    # Fanvue endpoint – this is a common pattern, check their dev portal
    resp = requests.post("https://api.fanvue.com/v1/posts", json=payload, headers=headers)
    return resp.json()
