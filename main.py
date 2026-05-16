import os
import random
import requests
import base64
from generate_image import generate_fashion_images
from generate_video import create_transition_video
from generate_caption import create_caption
from safety_check import is_safe
from post_fanvue import post_to_fanvue
from post_social import post_to_instagram, post_to_tiktok

def main():
    print("🚀 Starting daily influencer content generation...")

    # 1. Create an outfit sequence for "dress up with me"
    styles = [
        "a beautiful woman wearing a casual summer dress in a brunch cafe",
        "the same woman in a sexy leather outfit at a rooftop bar",
        "the same woman in an elegant red dress at a fancy restaurant"
    ]
    images = []
    for i, style in enumerate(styles):
        img_url = generate_fashion_images(style)
        if img_url:
            # Download the image to memory (we'll need it for video and posting)
            resp = requests.get(img_url)
            if resp.status_code == 200:
                image_bytes = resp.content
                with open(f"outfit_{i+1}.jpg", "wb") as f:
                    f.write(image_bytes)
                images.append(f"outfit_{i+1}.jpg")
                print(f"✅ Image {i+1} generated")
            else:
                print("❌ Failed to download image")
        else:
            print("❌ Image generation failed")

    if len(images) < 3:
        print("Not enough images, aborting.")
        return

    # 2. Safety check (SFW) – crucial!
    for img_path in images:
        if not is_safe(img_path):
            print(f"⚠️ Unsafe content detected in {img_path}, aborting.")
            return

    # 3. Create a short video (slideshow with transitions)
    video_path = create_transition_video(images, output="outfit_video.mp4")
    print(f"🎬 Video created: {video_path}")

    # 4. Generate a caption
    caption = create_caption("A day of outfit changes from brunch to dinner")
    print(f"💬 Caption: {caption}")

    # 5. Post to Fanvue (primary monetization)
    # We'll post the first image as the main photo, and the video as extra
    with open(images[0], "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    with open(video_path, "rb") as f:
        video_data = base64.b64encode(f.read()).decode("utf-8")

    fanvue_result = post_to_fanvue(caption, image_data, video_data)
    print(f"📢 Fanvue post result: {fanvue_result}")

    # 6. Optional: also post to social media if keys are set
    if os.getenv("INSTAGRAM_ACCESS_TOKEN"):
        post_to_instagram(caption, images[0])
    if os.getenv("TIKTOK_ACCESS_TOKEN"):
        post_to_tiktok(caption, video_path)

if __name__ == "__main__":
    main()
