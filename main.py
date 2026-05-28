import os
import requests
from generate_image import generate_fashion_images
from generate_video import create_transition_video
from generate_caption import create_caption
from safety_check import is_safe
from post_to_social import post_to_social

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

    # 2. Safety check (SFW)
    for img_path in images:
        if not is_safe(img_path):
            print(f"⚠️ Unsafe content detected in {img_path}, aborting.")
            return

    # 3. Create a short video (slideshow with fade)
    #    We still generate it, but we won't send it on the free plan.
    video_path = create_transition_video(images, output="outfit_video.mp4")
    print(f"🎬 Video created: {video_path}")

    # 4. Generate a caption
    caption = create_caption("A day of outfit changes from brunch to dinner")
    print(f"💬 Caption: {caption}")

    # 5. Post to all linked social media via Ayrshare
    #    IMPORTANT: video_path set to None because free plan only allows images.
    if os.getenv("AYRSHARE_API_KEY"):
        post_to_social(caption, images[0], video_path=None)
    else:
        print("⚠️ AYRSHARE_API_KEY not set, skipping social posts.")

if __name__ == "__main__":
    main()
