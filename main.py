import os, requests, random, subprocess, traceback
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
from generate_image import generate_fashion_images
from generate_caption import create_caption
from safety_check import is_safe
# ============================================================
# THEMES – identical to your previous one, no changes needed
# ============================================================
THEMES = {
    "grwm": {
        "title": "✨ GET READY WITH ME ✨",
        "video_style": "slow",
        "wiggle": False,
        "caption_context": "morning routine to a night out in three hot outfits",
        "scenes": [
            "wearing a silk pajama set, messy bun, holding a coffee mug, standing in a bright messy bedroom, morning sunlight",
            "applying facial cleanser, bathroom mirror reflection, white towel on head, spa vibe, clean skin, soft lighting",
            "standing in front of an open walk-in closet, holding two dresses, thinking pose, luxury fashion, daylight",
            "wearing a casual summer dress, full body mirror selfie, brunch cafe background, smiling, golden hour light",
            "wearing a sexy leather outfit, rooftop bar at sunset, city skyline view, confident pose, cocktail in hand",
            "wearing an elegant red dress, fine dining restaurant, sitting at a candlelit table, looking at camera, romantic atmosphere"
        ]
    },
    "dance": {
        "title": "💃 DANCE WITH ME 💃",
        "video_style": "fast",
        "wiggle": True,
        "caption_context": "new dance routine, feeling the beat",
        "scenes": [
            "mid-air jump, dance studio with neon lights, dynamic pose, sporty outfit, hair flying, action shot",
            "spinning on one leg, dance floor, blurry background, high energy, crop top and leggings",
            "hip-hop stance, arms crossed, streetwear, graffiti wall, cool expression, low angle",
            "contemporary dance pose, flowy dress, empty theatre stage, dramatic lighting, silhouette effect",
            "ballet leap, tutu, soft pink light, dreamy atmosphere, pointed toes",
            "club dance, hands up, DJ lights, smiling, carefree, glitter outfit"
        ]
    },
    "music_video": {
        "title": "🎤 MUSIC VIDEO VIBES 🎤",
        "video_style": "medium",
        "wiggle": False,
        "caption_context": "new music video look, feeling like a pop star",
        "scenes": [
            "holding a vintage microphone, recording studio, headphones around neck, serious expression",
            "singing passionately, rain falling on a city street at night, leather jacket, cinematic lighting",
            "dramatic close-up, wind blowing hair, desert highway at sunset, bohemian outfit",
            "dancing in an empty warehouse, laser lights, futuristic outfit, sci-fi vibe",
            "sitting on a car hood, looking at the camera, starry night sky, cool denim look",
            "confetti falling, cheering crowd blurred behind, performer on stage, arms wide open"
        ]
    },
    "fashion_haul": {
        "title": "🛍️ FASHION HAUL 🛍️",
        "video_style": "slow",
        "wiggle": False,
        "caption_context": "shopping haul, trying on new fits",
        "scenes": [
            "holding many shopping bags, entering a chic boutique, excited face, sunny day",
            "holding up a dress in front of a mirror, fitting room, smiling, natural light",
            "trying on a stylish coat, twirling, full body shot, city street background",
            "sitting cross-legged with shoes, accessories, and clothes laid out, flat lay style",
            "wearing a glamorous evening gown, walking down a marble staircase, luxury hotel",
            "showing off a casual streetwear look, posing against a brick wall, cool sunglasses"
        ]
    },
    "vlog": {
        "title": "📱 A DAY IN MY LIFE 📱",
        "video_style": "slow",
        "wiggle": False,
        "caption_context": "come with me through my day",
        "scenes": [
            "waking up, stretching in bed, white sheets, sunlight, natural no-makeup look",
            "making a smoothie in the kitchen, healthy lifestyle, messy bun, smiling",
            "working on a laptop at a cute coffee shop, latte art, casual sweater, focused",
            "walking a dog in the park, candid laugh, autumn leaves, activewear",
            "meeting friends for lunch, outdoor restaurant, talking and laughing, natural candid",
            "sunset yoga on a rooftop, peaceful expression, workout set, golden hour glow"
        ]
    },
    "fitness": {
        "title": "🏋️‍♀️ WORKOUT WITH ME 🏋️‍♀️",
        "video_style": "fast",
        "wiggle": False,
        "caption_context": "morning workout, staying fit",
        "scenes": [
            "lacing up trainers, gym locker room, determined look, sportswear",
            "doing squats with a barbell, gym floor, focused face, strong lighting",
            "jumping rope, rooftop, city view, sunset, athletic body",
            "sipping from a protein shake, resting on a yoga mat, sweaty glow, smile",
            "plank pose, beach at sunrise, core strength, serene expression",
            "stretching after workout, peaceful studio, natural light, toned body"
        ]
    },
    "cooking": {
        "title": "🍳 COOK WITH ME 🍳",
        "video_style": "slow",
        "wiggle": False,
        "caption_context": "cooking a delicious meal from scratch",
        "scenes": [
            "tying an apron, bright kitchen, fresh ingredients on counter, smiling",
            "chopping vegetables, close up hands, knife skills, natural lighting",
            "stirring a pan, steam rising, cozy kitchen atmosphere, soft focus background",
            "tasting sauce from a wooden spoon, happy expression, chef vibe",
            "plating a beautiful dish, overhead shot, restaurant quality, colorful",
            "sitting at a dining table with the finished meal, candlelight, proud smile"
        ]
    },
    "beach_day": {
        "title": "🌊 BEACH DAY 🌊",
        "video_style": "slow",
        "wiggle": False,
        "caption_context": "sun, sand, and sea",
        "scenes": [
            "walking along the shoreline, waves lapping, white bikini, wide brim hat, carefree",
            "lying on a beach towel, sunglasses, reading a book, turquoise water behind",
            "playing with a beach ball, laughing, splashing water, dynamic action",
            "sitting on a swing tied to a palm tree, sunset, silhouette, dreamy",
            "collecting seashells, crouching, soft sand, curious expression",
            "running into the ocean, splashing, back view, golden hour, freedom"
        ]
    },
    "travel": {
        "title": "✈️ TRAVEL DIARIES ✈️",
        "video_style": "medium",
        "wiggle": False,
        "caption_context": "jet-setting to a new destination",
        "scenes": [
            "at the airport, pulling a suitcase, chic travel outfit, sunglasses, excitement",
            "boarding pass in hand, looking out of airplane window, clouds, wanderlust",
            "arriving at a luxury hotel, lobby, marble floors, bellhop, awe expression",
            "exploring a charming old town, cobblestone streets, flowy dress, pointing at architecture",
            "enjoying local food at a street market, exotic dishes, happy tasting face",
            "sunset from a rooftop infinity pool, bikini, holding a cocktail, breathtaking view"
        ]
    },
    "night_out": {
        "title": "🥂 NIGHT OUT 🥂",
        "video_style": "fast",
        "wiggle": True,
        "caption_context": "girls' night out, let's party",
        "scenes": [
            "getting ready with friends, bathroom mirror, makeup, champagne glasses",
            "clinking cocktails at a neon-lit bar, laughing, sequin dress",
            "dancing in a club, laser lights, hands up, surrounded by people, euphoric",
            "taking a selfie with friends, flash, pouty lips, night out vibes",
            "walking through the city at night, high heels, confident stride, street lights",
            "eating late-night pizza slice, messy hair, laughing, candid"
        ]
    },
    "coffee_date": {
        "title": "☕ COFFEE DATE ☕",
        "video_style": "slow",
        "wiggle": False,
        "caption_context": "cute coffee shop moment",
        "scenes": [
            "entering a cozy café, bell on door, warm lighting, cute outfit",
            "ordering at the counter, pointing at menu, smiling at barista",
            "holding a latte with foam art, sitting by window, rain outside, peaceful",
            "reading a book, glasses on, soft sweater, ambiance",
            "laughing with a friend across the table, candid, two cups",
            "walking out with coffee in hand, autumn leaves, scarf, happy"
        ]
    },
    "self_care": {
        "title": "🛁 SELF CARE SUNDAY 🛁",
        "video_style": "slow",
        "wiggle": False,
        "caption_context": "pampering myself, relaxing",
        "scenes": [
            "lighting candles, bathroom, bathrobe, calm smile",
            "applying a face mask, green clay, cucumber slices, funny/relaxed",
            "soaking in a bubble bath, rose petals, reading a magazine, serene",
            "doing skincare routine, serums, jade roller, glowing skin",
            "wrapped in a fluffy towel, hair turban, drinking tea",
            "meditating on a yoga mat, incense, sunlight, peaceful"
        ]
    },
    "photoshoot": {
        "title": "📸 BEHIND THE SCENES 📸",
        "video_style": "medium",
        "wiggle": False,
        "caption_context": "professional photoshoot day",
        "scenes": [
            "makeup artist touching up, mirror, bright lights, model expression",
            "photographer adjusting camera, studio backdrop, striking a pose",
            "changing outfits behind a screen, peeking out, playful",
            "high-fashion pose, wind machine, hair blowing, fierce look",
            "reviewing photos on camera screen, laughing with crew",
            "final shot, confetti, celebration, champagne pop"
        ]
    },
    "shopping": {
        "title": "🛒 COME SHOP WITH ME 🛒",
        "video_style": "slow",
        "wiggle": False,
        "caption_context": "mall haul and trying on clothes",
        "scenes": [
            "entering a luxury boutique, door opening, excited face",
            "browsing racks, holding up a cute top, thinking",
            "trying on heels, sitting on a bench, mirror reflection",
            "showing off a handbag, posing, full body mirror",
            "carrying multiple shopping bags, smiling, successful spree",
            "iced coffee break, sitting at a café, bags around, happy"
        ]
    },
    "pet_day": {
        "title": "🐶 DAY WITH MY PET 🐶",
        "video_style": "slow",
        "wiggle": False,
        "caption_context": "spending quality time with my fur baby",
        "scenes": [
            "cuddling a golden retriever on the couch, messy hair, morning light",
            "playing fetch in the park, running, laughing, green grass",
            "giving the dog a bath, suds, wet fur, funny expression",
            "dressing the pet in a cute bandana, posing together",
            "sharing a pup-friendly ice cream, tongue out, adorable",
            "napping together on a picnic blanket, sunny day, peaceful"
        ]
    },
    "artistic": {
        "title": "🎨 CREATIVE SHOOT 🎨",
        "video_style": "medium",
        "wiggle": False,
        "caption_context": "expressing myself through art",
        "scenes": [
            "standing in front of a colorful mural, paint-splattered overalls, brush in hand",
            "throwing paint at a canvas, action shot, vibrant colors, joyful",
            "posing with a finished painting, gallery setting, sophisticated dress",
            "drawing in a sketchbook, café, pencil behind ear, thoughtful",
            "spinning in a room full of hanging art, flowy skirt, whimsical",
            "painting on a large window, backlit, sunset, creative"
        ]
    },
    "rainy_day": {
        "title": "☔ RAINY DAY VIBES ☔",
        "video_style": "slow",
        "wiggle": False,
        "caption_context": "cozy rainy day at home",
        "scenes": [
            "looking out a rain-streaked window, holding a mug, cozy sweater",
            "curled up on a couch with a blanket, reading a book, soft lamp light",
            "baking cookies, flour on nose, cute apron, warm kitchen",
            "watching a movie with popcorn, laughing, fluffy socks",
            "painting nails, sitting on the floor, cozy rug, relaxing",
            "jumping in a puddle outside, yellow raincoat, playful, smile"
        ]
    },
    "sunset": {
        "title": "🌅 SUNSET CHASING 🌅",
        "video_style": "slow",
        "wiggle": False,
        "caption_context": "chasing golden hour",
        "scenes": [
            "driving a convertible, hair blowing, sunglasses, open road, golden light",
            "standing on a hilltop, arms wide open, sunflare, maxi dress",
            "walking through a field of wildflowers, back view, sunset glow",
            "sitting on a dock, feet dangling, lake, orange sky",
            "blowing dandelion seeds, close up, magical light",
            "lying on a blanket, looking at the stars appearing, peaceful smile"
        ]
    },
    "concert": {
        "title": "🎸 CONCERT NIGHT 🎸",
        "video_style": "fast",
        "wiggle": True,
        "caption_context": "live music with friends",
        "scenes": [
            "waiting in line outside venue, band tee, excited, dusk",
            "holding a ticket, entering the crowd, lights, anticipation",
            "singing along, arms raised, stage lights, euphoric",
            "on someone's shoulders, crowd surfing, wild",
            "band playing, back view, silhouettes, dramatic lighting",
            "after the show, sweaty, happy, group selfie outside"
        ]
    },
    "birthday": {
        "title": "🎂 BIRTHDAY GIRL 🎂",
        "video_style": "slow",
        "wiggle": False,
        "caption_context": "celebrating my special day",
        "scenes": [
            "waking up to balloons, messy bed, surprised happy face",
            "opening a gift, ribbon, excited expression",
            "blowing out candles on a cake, dark room, candlelight glow",
            "dancing with friends, party decorations, confetti",
            "making a wish, eyes closed, hands together, smiling",
            "thank you pose, holding a sign or card, love hearts"
        ]
    }
}
def ultra_6k_sharpen(path):
    """
    Upscale to 5760x5760 (6K), then apply aggressive sharpening and save at quality 100.
    Output: 10-15 MB per image.
    """
    try:
        img = Image.open(path).convert("RGB")
        # Upscale to 6K using Lanczos
        img = img.resize((5760, 5760), Image.LANCZOS)

        # Stage 1: Strong unsharp mask (radius 1.0, amount 400%)
        img = img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=400, threshold=0))

        # Stage 2: High-pass overlay for micro-contrast
        arr = np.array(img, dtype=np.float32)
        blurred = np.array(img.filter(ImageFilter.GaussianBlur(radius=8)), dtype=np.float32)
        high_pass = arr - blurred + 128.0
        sharpened = np.clip(arr + (high_pass - 128.0) * 0.6, 0, 255).astype(np.uint8)
        img = Image.fromarray(sharpened)

        # Stage 3: Contrast boost
        img = ImageEnhance.Contrast(img).enhance(1.15)

        # Stage 4: Saturation boost (HSV)
        hsv = img.convert("HSV")
        h, s, v = hsv.split()
        s = s.point(lambda i: min(255, int(i * 1.2)))
        img = Image.merge("HSV", (h, s, v)).convert("RGB")

        # Save with maximum quality, no chroma subsampling
        img.save(path, quality=100, subsampling=0)
        size_mb = os.path.getsize(path) / (1024*1024)
        print(f"🔪 6K ultra-sharp: {path} ({size_mb:.1f} MB)")
    except Exception as e:
        print(f"⚠️ Sharpening failed for {path}: {e}")

# ================== RELIABLE VIDEO (FFmpeg slideshow + fade) ==================
def create_slideshow_video(image_paths, title_text, video_style, output):
    """
    Create a video:
    1. Title card (2 sec)
    2. Each image displayed for style-dependant duration
    3. Fade in at start, fade out at end.
    No complex crossfade – stable and always works.
    """
    # Title image
    title_img = Image.new("RGB", (1080, 1350), (0, 0, 0))
    draw = ImageDraw.Draw(title_img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), title_text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(((1080 - tw)//2, (1350 - th)//2), title_text,
              fill=(255,255,255), font=font, stroke_width=3, stroke_fill=(0,0,0))
    title_path = "title.png"
    title_img.save(title_path)

    # Durations
    if video_style == "fast":
        img_dur = 1.5
    elif video_style == "medium":
        img_dur = 2.0
    else:
        img_dur = 2.5
    title_dur = 2.0
    # Total video duration
    total_dur = title_dur + len(image_paths) * img_dur

    # Build concat file list (title + images) with durations
    with open("concat_list.txt", "w") as f:
        f.write(f"file '{title_path}'\n")
        f.write(f"duration {title_dur}\n")
        for img in image_paths:
            f.write(f"file '{img}'\n")
            f.write(f"duration {img_dur}\n")
        # Last image must be listed again without duration
        f.write(f"file '{image_paths[-1]}'\n")

    # First pass: create raw concatenated video
    temp_raw = "temp_raw.mp4"
    cmd1 = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", "concat_list.txt",
        "-vf", "scale=1080:1350:force_original_aspect_ratio=1,pad=1080:1350:(ow-iw)/2:(oh-ih)/2,setsar=1",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "fast", "-crf", "20",
        "-r", "24",
        temp_raw
    ]
    subprocess.run(cmd1, check=True)

    # Second pass: apply fade in/out to the whole video
    fade_cmd = [
        "ffmpeg", "-y",
        "-i", temp_raw,
        "-vf", f"fade=in:0:12,fade=out:{int((total_dur-1)*24)}:12",  # 0.5 sec fade
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "fast", "-crf", "22",
        output
    ]
    subprocess.run(fade_cmd, check=True)
    os.remove(temp_raw)
    print(f"🎬 Video created: {output}")

# ================== MAIN ==================
def main():
    print("🚀 Starting daily influencer content generation...")
    theme_name = random.choice(list(THEMES.keys()))
    theme = THEMES[theme_name]
    print(f"🎭 Theme: {theme_name} – {theme['title']}")

    daily_seed = random.randint(1, 100000)
    image_paths = []

    for i, prompt in enumerate(theme["scenes"]):
        url = generate_fashion_images(prompt, seed=daily_seed, width=2048, height=2048)
        resp = requests.get(url)
        if resp.status_code == 200:
            path = f"image_{i+1}.jpg"
            with open(path, "wb") as f:
                f.write(resp.content)
            ultra_6k_sharpen(path)   # 6K upscale + extreme sharpening
            image_paths.append(path)
            print(f"✅ Image {i+1} saved & enhanced")
        else:
            print(f"❌ Failed to download image {i+1}")

    if len(image_paths) < 6:
        print("Not enough images, aborting.")
        return

    # Safety check
    for img in image_paths:
        if not is_safe(img):
            print(f"⚠️ Unsafe content in {img}, aborting.")
            return

    # Create video (reliable slideshow + fade)
    video_output = "daily_video.mp4"
    try:
        create_slideshow_video(image_paths, theme["title"], theme["video_style"], video_output)
    except Exception as e:
        print(f"❌ Video failed: {e}")
        traceback.print_exc()
        # Fallback black video
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1080x1350:d=3",
            "-c:v", "libx264", video_output
        ], check=True)
        print("⚠️ Fallback black video created.")

    # Caption
    caption = create_caption(theme["caption_context"])
    with open("caption.txt", "w") as f:
        f.write(caption)
    print(f"💬 Caption: {caption}")

    print("📦 Content ready. Email splitting will be handled by send_emails.py.")

if __name__ == "__main__":
    main()
