import os, requests, random, subprocess, traceback
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
def realistic_enhance(path):
    """
    Upscale to 2730x3640 (perfect 3:4 portrait), apply natural sharpening,
    and boost contrast slightly to mimic phone camera processing.
    Output: 8-10 MB, crisp but not artificial.
    """
    try:
        img = Image.open(path).convert("RGB")
        # Upscale to 3:4 portrait (2730x3640) using Lanczos
        img = img.resize((2730, 3640), Image.LANCZOS)

        # Mild unsharp mask (radius 2.0, amount 120%) – enhances clarity without halos
        img = img.filter(ImageFilter.UnsharpMask(radius=2.0, percent=150, threshold=3))

        # Subtle contrast boost (1.08) to make the image pop
        img = ImageEnhance.Contrast(img).enhance(1.08)

        # Save at 95% quality – good balance between size and detail
        img.save(path, quality=95, subsampling=0)
        size_mb = os.path.getsize(path) / (1024*1024)
        print(f"📱 Realistic enhanced: {path} ({size_mb:.1f} MB)")
    except Exception as e:
        print(f"⚠️ Enhancement failed for {path}: {e}")

# ================== RELIABLE VIDEO (ZOOM + CROSSFADE) ==================
def create_realistic_video(image_paths, title_text, video_style, output):
    """
    Build a video with:
    - Title card (2 sec)
    - Each image with a slow zoom (Ken Burns) – 4 sec for slow, 3 for medium, 2.5 for fast
    - Smooth crossfade (0.5 sec) between all clips
    - High bitrate (10 Mbps) to ensure 20-30 MB final size.
    """
    # Durations
    if video_style == "fast":
        img_dur = 2.5
    elif video_style == "medium":
        img_dur = 3.0
    else:
        img_dur = 4.0   # GRWM/vlog
    title_dur = 2.0
    fade_dur = 0.5

    # Create title image
    title_img = Image.new("RGB", (1080, 1350), (0, 0, 0))
    draw = ImageDraw.Draw(title_img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), title_text, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text(((1080-tw)//2, (1350-th)//2), title_text,
              fill=(255,255,255), font=font, stroke_width=3, stroke_fill=(0,0,0))
    title_path = "title.png"
    title_img.save(title_path)

    # Step 1: Generate individual zoomed clips for each image (including title)
    clips = []  # list of temporary filenames
    # Title (no zoom, just static) – 2 sec
    title_clip = "title_clip.mp4"
    cmd_title = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(title_dur), "-i", title_path,
        "-vf", "scale=1080:1350:force_original_aspect_ratio=1,pad=1080:1350:(ow-iw)/2:(oh-ih)/2,setsar=1",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "fast", "-crf", "18",
        "-t", str(title_dur),
        title_clip
    ]
    subprocess.run(cmd_title, check=True)
    clips.append(title_clip)

    # For each image, apply zoompan to simulate slow zoom
    for i, img_path in enumerate(image_paths):
        clip_name = f"clip_{i}.mp4"
        # Zoom from 1.0 to 1.1 over img_dur seconds, with slight random pan
        pan_x = random.uniform(-0.02, 0.02)  # small horizontal shift
        pan_y = random.uniform(-0.02, 0.02)  # small vertical shift
        zoom_expr = f"zoom+0.1/{img_dur}"
        x_expr = f"iw/2-(iw/zoom/2)+{pan_x}*on"
        y_expr = f"ih/2-(ih/zoom/2)+{pan_y}*on"
        cmd_zoom = [
            "ffmpeg", "-y",
            "-loop", "1", "-t", str(img_dur), "-i", img_path,
            "-vf",
            f"scale=1080:1350:force_original_aspect_ratio=1,pad=1080:1350:(ow-iw)/2:(oh-ih)/2,setsar=1,"
            f"zoompan=z='{zoom_expr}':x='{x_expr}':y='{y_expr}':d={img_dur*24}:s=1080x1350,"
            f"fps=24",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-preset", "fast", "-crf", "18",
            "-t", str(img_dur),
            clip_name
        ]
        subprocess.run(cmd_zoom, check=True)
        clips.append(clip_name)

    # Step 2: Concatenate all clips with crossfade
    # We'll use the concat protocol with a list file containing durations and then apply xfade via filter_complex
    # Simpler: use concat with a filter complex that adds xfade. We'll build a single ffmpeg command.
    # First, create a file list for concat demuxer (but xfade won't work with that). Better: use multiple inputs.
    # Let's build the complex filter manually using the clips we just generated.
    input_args = []
    for clip in clips:
        input_args.extend(["-i", clip])

    # Build filter complex: start with [0:v] (title), then for each subsequent clip, xfade with previous
    filter_parts = []
    filter_parts.append(f"[0:v]setpts=PTS-STARTPTS[v0];")
    for i in range(1, len(clips)):
        filter_parts.append(f"[{i}:v]setpts=PTS-STARTPTS[v{i}];")
    # Now chain xfades
    prev = "v0"
    offset = title_dur
    for i in range(1, len(clips)):
        next_label = f"v{i}"
        filter_parts.append(
            f"[{prev}][{next_label}]xfade=transition=fade:duration={fade_dur}:offset={offset}[{prev}{i}];"
        )
        prev = f"{prev}{i}"
        offset += img_dur - fade_dur  # adjust for overlap
    filter_parts.append(f"[{prev}]format=yuv420p[vout]")

    filter_complex = "".join(filter_parts)

    cmd_concat = [
        "ffmpeg", "-y",
        *input_args,
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-b:v", "10M",
        "-maxrate", "12M",
        "-bufsize", "20M",
        "-r", "24",
        output
    ]
    print("🎥 Building final video with crossfade...")
    subprocess.run(cmd_concat, check=True)
    # Clean up temporary clips
    for clip in clips:
        os.remove(clip)
    os.remove(title_path)
    size_mb = os.path.getsize(output) / (1024*1024)
    print(f"✅ Video created: {output} ({size_mb:.1f} MB)")

# ================== MAIN ==================
def main():
    print("🚀 Starting daily influencer content...")
    theme_name = random.choice(list(THEMES.keys()))
    theme = THEMES[theme_name]
    print(f"🎭 Theme: {theme_name} – {theme['title']}")

    daily_seed = random.randint(1, 100000)
    image_paths = []

    for i, prompt in enumerate(theme["scenes"]):
        # Generate at 2048x2730 (3:4) for better composition
        url = generate_fashion_images(prompt, seed=daily_seed, width=2048, height=2730)
        resp = requests.get(url)
        if resp.status_code == 200:
            path = f"image_{i+1}.jpg"
            with open(path, "wb") as f:
                f.write(resp.content)
            realistic_enhance(path)   # upscale + natural sharpening
            image_paths.append(path)
            print(f"✅ Image {i+1} saved")
        else:
            print(f"❌ Failed to download image {i+1}")

    if len(image_paths) < 6:
        print("Not enough images, aborting.")
        return

    for img in image_paths:
        if not is_safe(img):
            print(f"⚠️ Unsafe content in {img}, aborting.")
            return

    # Create video (reliable zoom + crossfade)
    video_output = "daily_video.mp4"
    try:
        create_realistic_video(image_paths, theme["title"], theme["video_style"], video_output)
    except Exception as e:
        print(f"❌ Video error: {e}")
        traceback.print_exc()
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1080x1350:d=3",
            "-c:v", "libx264", video_output
        ], check=True)
        print("⚠️ Fallback black video created.")

    caption = create_caption(theme["caption_context"])
    with open("caption.txt", "w") as f:
        f.write(caption)
    print(f"💬 Caption: {caption}")

    print("📦 Content ready for email delivery.")

if __name__ == "__main__":
    main()
