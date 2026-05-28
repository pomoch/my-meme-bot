import requests
import os
import base64

def post_to_social(caption, image_path, video_path=None):
    """
    Post to ALL linked social platforms via Ayrshare.
    Automatically distributes to Instagram, TikTok, X, Facebook, LinkedIn,
    Pinterest, Reddit, YouTube, etc. – whatever you've linked in your dashboard.
    """
    api_key = os.getenv("AYRSHARE_API_KEY")
    if not api_key:
        print("⚠️ AYRSHARE_API_KEY not found.")
        return

    url = "https://app.ayrshare.com/api/post"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Convert image to base64 data URI
    with open(image_path, "rb") as img_file:
        image_b64 = base64.b64encode(img_file.read()).decode("utf-8")
    image_data_uri = f"data:image/jpeg;base64,{image_b64}"

    payload = {
        "post": caption,
        "platforms": ["instagram", "tiktok", "x", "facebook", "linkedin",
                      "pinterest", "reddit", "youtube"],
        "mediaUrls": [image_data_uri]
    }

    # If video exists, replace media with video and add optional thumbnail
    if video_path:
        with open(video_path, "rb") as vid_file:
            video_b64 = base64.b64encode(vid_file.read()).decode("utf-8")
        video_data_uri = f"data:video/mp4;base64,{video_b64}"
        payload["mediaUrls"] = [video_data_uri]
        # Optionally set a custom thumbnail (the first outfit image)
        payload["thumbNail"] = image_data_uri

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("✅ Successfully posted to all selected platforms!")
            print(response.json())
        else:
            print(f"❌ Ayrshare API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Failed to send post: {e}")
