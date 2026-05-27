import requests

def post_to_instagram(image_path, caption, access_token, ig_user_id):
    """
    Post a single image to Instagram using the Graph API.
    Requires a public URL for the image; we'll use a free temporary upload.
    """
    # Step 1: Upload the image to a temporary hosting (we'll use 0x0.st, free and direct)
    with open(image_path, 'rb') as f:
        upload_resp = requests.post('https://0x0.st', files={'file': f})
    if upload_resp.status_code != 200:
        return {"error": "Image upload failed", "details": upload_resp.text}
    image_url = upload_resp.text.strip()
    print(f"📤 Image uploaded to {image_url}")

    # Step 2: Create a media container
    container_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media"
    params = {
        "image_url": image_url,
        "caption": caption,
        "access_token": access_token
    }
    resp = requests.post(container_url, data=params)
    if resp.status_code != 200:
        return {"error": "Media container creation failed", "details": resp.json()}
    container_id = resp.json().get("id")
    print(f"📦 Container ID: {container_id}")

    # Step 3: Publish the container
    publish_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media_publish"
    publish_params = {
        "creation_id": container_id,
        "access_token": access_token
    }
    publish_resp = requests.post(publish_url, data=publish_params)
    return publish_resp.json()
