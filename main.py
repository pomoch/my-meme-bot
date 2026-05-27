import os
import requests
import base64
from generate_image import generate_fashion_images
from generate_video import create_transition_video
from generate_caption import create_caption
from safety_check import is_safe
from post_instagram import post_to_instagram
from post_tiktok import post_to_tiktok

def main():
    print("🚀 Starting daily AI influencer content generation...")

    # 1. Create outfit images
    styles = [
        "a beautiful woman wearing a casual summer dress in a brunch cafe",
        "the same woman in a sexy leather outfit at a rooftop bar",
        "the same woman in an elegant red dress at a fancy restaurant"
    ]
    images = []
    for i, style in enumerate(styles):
        img_url = generate_fashion_images(style)
        if img_url:
            resp = requests.get(img_url)
            if resp.status_code == 200:
                with open(f"outfit_{i+1}.jpg", "wb") as f:
                    f.write(resp.content)
                images.append(f"outfit_{i+1}.jpg")
                print(f"✅ Image {i+1} generated")
            else:
                print("❌ Failed to download image")
        else:
            print("❌ Image generation failed")

    if len(images) < 3:
        print("Not enough images, aborting.")
        return

    # 2. Safety check (SFW) – still crucial for Instagram/TikTok policies
    for img_path in images:
        if not is_safe(img_path):
            print(f"⚠️ Unsafe content detected in {img_path}, aborting.")
            return

    # 3. Create a short video (slideshow)
    video_path = create_transition_video(images, output="outfit_video.mp4")
    print(f"🎬 Video created: {video_path}")

    # 4. Generate a caption
    caption = create_caption("A day of outfit changes from brunch to dinner")
    print(f"💬 Caption: {caption}")

    # 5. Post to Instagram (image + caption)
    if os.getenv("INSTAGRAM_ACCESS_TOKEN") and os.getenv("INSTAGRAM_USER_ID"):
        result = post_to_instagram(
            image_path=images[0],
            caption=caption,
            access_token=os.getenv("INSTAGRAM_ACCESS_TOKEN"),
            ig_user_id=os.getenv("INSTAGRAM_USER_ID")
        )
        print(f"📸 Instagram post result: {result}")
    else:
        print("⚠️ Instagram token or user ID not set, skipping Instagram post.")

    # 6. Post to TikTok (video + caption)
    if os.getenv("TIKTOK_ACCESS_TOKEN") and os.getenv("TIKTOK_OPEN_ID"):
        result = post_to_tiktok(
            video_path=video_path,
            caption=caption,
            access_token=os.getenv("TIKTOK_ACCESS_TOKEN"),
            open_id=os.getenv("TIKTOK_OPEN_ID")
        )
        print(f"🎵 TikTok post result: {result}")
    else:
        print("⚠️ TikTok token or open ID not set, skipping TikTok post.")

if __name__ == "__main__":
    main()
