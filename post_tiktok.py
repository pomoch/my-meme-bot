import requests
import time
import os

def post_to_tiktok(video_path, caption, access_token, open_id):
    """
    Upload and post a video to TikTok using the Content Posting API (v2).
    This uses the direct upload flow.
    """
    # Step 1: Initialize upload
    init_url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    file_size = os.path.getsize(video_path)
    init_body = {
        "post_info": {
            "title": caption,
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
            "video_cover_timestamp_ms": 1000  # uses a frame as cover
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": file_size,
            "chunk_size": file_size,  # upload in one chunk if < 50MB
            "total_chunk_count": 1
        }
    }
    resp = requests.post(init_url, json=init_body, headers=headers)
    if resp.status_code not in (200, 201):
        return {"error": "Init failed", "details": resp.json()}
    data = resp.json().get("data", {})
    upload_url = data["upload_url"]
    publish_id = data["publish_id"]
    print(f"📤 TikTok upload initialized, publish_id: {publish_id}")

    # Step 2: Upload video bytes
    with open(video_path, "rb") as f:
        video_bytes = f.read()
    upload_headers = {
        "Content-Type": "video/mp4",
        "Content-Length": str(file_size),
        "Authorization": f"Bearer {access_token}"
    }
    upload_resp = requests.put(upload_url, data=video_bytes, headers=upload_headers)
    if upload_resp.status_code not in (200, 201):
        return {"error": "Upload failed", "details": upload_resp.text}

    # Step 3: Check status / trigger publish (sometimes done automatically after upload)
    status_url = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"
    status_body = {"publish_id": publish_id}
    # Poll until published
    for _ in range(5):
        time.sleep(3)
        status_resp = requests.post(status_url, json=status_body, headers=headers)
        if status_resp.status_code == 200:
            status_data = status_resp.json().get("data", {})
            if status_data.get("status") == "PUBLISH_COMPLETE":
                return {"success": True, "publish_id": publish_id}
        print("⏳ Checking status...")
    return {"error": "Publish status unknown", "details": status_resp.json()}
