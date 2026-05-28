import os
import requests
from generate_image import generate_fashion_images
from generate_video import create_transition_video
from generate_caption import create_caption
from safety_check import is_safe

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
    video_path = create_transition_video(images, output="outfit_video.mp4")
    print(f"🎬 Video created: {video_path}")

    # 4. Generate a caption (just for info, we'll include it in the email body)
    caption = create_caption("A day of outfit changes from brunch to dinner")
    with open("caption.txt", "w") as f:
        f.write(caption)
    print(f"💬 Caption saved: {caption}")

    # All files (outfit_1.jpg, outfit_2.jpg, outfit_3.jpg, outfit_video.mp4, caption.txt)
    # will be available for the next step (email).

if __name__ == "__main__":
    main()
