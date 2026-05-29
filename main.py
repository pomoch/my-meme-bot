import os, requests, random, subprocess, traceback, math
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont, ImageColor
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
def upscale_with_waifu2x(path):
    """
    Use waifu2x model to upscale 2x and reduce noise, then resize to 3000x4000.
    This gives photo‑level sharpness.
    """
    try:
        img = cv2.imread(path)
        # Waifu2x model (anime‑style but works great on skin)
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        sr.readModel("waifu2x_photo.onnx")   # we'll download it below
        sr.setModel("waifu2x", 2)
        upscaled = sr.upsample(img)
        # Resize to exact 3000x4000 using Lanczos
        upscaled = cv2.resize(upscaled, (3000, 4000), interpolation=cv2.INTER_LANCZOS4)
        # Convert to PIL for mild sharpening and save
        upscaled_rgb = cv2.cvtColor(upscaled, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(upscaled_rgb)
        pil_img = pil_img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=150, threshold=2))
        pil_img.save(path, quality=100, subsampling=0)
        print(f"🔍 Upscaled: {path} ({os.path.getsize(path)/1024**2:.1f} MB)")
    except Exception as e:
        print(f"⚠️ Upscale failed, using fallback sharpening: {e}")
        # Fallback: normal Lanczos resize
        img = Image.open(path).convert("RGB")
        img = img.resize((3000, 4000), Image.LANCZOS)
        img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=200, threshold=2))
        img.save(path, quality=100, subsampling=0)

# ================== DOWNLOAD WAIFU2X MODEL (once) ==================
def ensure_waifu2x_model():
    if not os.path.exists("waifu2x_photo.onnx"):
        print("⬇️ Downloading waifu2x model...")
        url = "https://github.com/nagadomi/waifu2x/raw/master/models/upconv_7_photo/upconv_7_photo.onnx"
        r = requests.get(url)
        with open("waifu2x_photo.onnx", "wb") as f:
            f.write(r.content)
        print("✅ Model downloaded.")

# ================== STOP‑MOTION PHONE VIDEO ==================
def create_motion_video(image_sets, title_text, video_style, output):
    """
    Each 'scene' has 3 images (slight pose differences).
    We play them at 8 FPS to simulate low‑frame‑rate phone recording.
    Fast cuts, camera shake, phone UI.
    """
    if video_style == "fast":
        scene_dur = 0.8   # per scene
    elif video_style == "medium":
        scene_dur = 1.0
    else:
        scene_dur = 1.2
    title_dur = 2.0
    fps = 8   # low frame rate for authentic phone look

    # Title image
    title_img = Image.new("RGB", (1080, 1350), (0,0,0))
    draw = ImageDraw.Draw(title_img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0,0), title_text, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text(((1080-tw)//2, (1350-th)//2), title_text, fill="white", font=font, stroke_width=3, stroke_fill="black")
    title_path = "title.png"
    title_img.save(title_path)

    clip_files = []

    # Title clip
    title_clip = "clip_title.mp4"
    run_ffmpeg([
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(title_dur), "-i", title_path,
        "-vf", "scale=1080:1350,setsar=1",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "fast", "-crf", "18",
        "-r", str(fps),
        title_clip
    ], "title")
    clip_files.append(title_clip)

    # For each scene, create a clip that cycles the 3 images
    for i, scene_imgs in enumerate(image_sets):
        clip_name = f"clip_scene_{i}.mp4"
        # Build input list: 3 images, looped to fill scene_dur
        input_args = []
        for img in scene_imgs:
            input_args.extend(["-loop", "1", "-t", str(scene_dur/3), "-i", img])
        # Filter complex: concat the three streams, then apply shake + phone UI
        filter_parts = []
        # First, trim each input to the right duration
        for j in range(3):
            filter_parts.append(f"[{j}:v]trim=duration={scene_dur/3},setpts=PTS-STARTPTS[v{j}];")
        # Concatenate
        filter_parts.append(f"[v0][v1][v2]concat=n=3:v=1:a=0,"
                            f"scale=1080:1350:force_original_aspect_ratio=1,"
                            f"pad=1080:1350:(ow-iw)/2:(oh-ih)/2,setsar=1,"
                            f"fps={fps},"
                            f"crop=iw-12:ih-12:random(0)*12:random(0)*12,"   # shake
                            f"scale=1080:1350,"
                            f"drawtext=text='REC ●  12:34  🔋 85%%':fontcolor=white:fontsize=24:x=20:y=20:box=1:boxcolor=black@0.4:boxborderw=5,"
                            f"format=yuv420p[vout]")
        filter_complex = "".join(filter_parts)
        run_ffmpeg([
            "ffmpeg", "-y",
            *input_args,
            "-filter_complex", filter_complex,
            "-map", "[vout]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-preset", "fast", "-crf", "18",
            "-r", str(fps),
            clip_name
        ], f"scene {i+1}")
        clip_files.append(clip_name)

    # Concatenate all scene clips
    concat_list = "concat_list.txt"
    with open(concat_list, "w") as f:
        for cf in clip_files:
            f.write(f"file '{cf}'\n")
    temp_concat = "temp_concat.mp4"
    run_ffmpeg([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_list,
        "-c", "copy",
        temp_concat
    ], "concat scenes")

    # Fade in/out
    total_dur = title_dur + len(image_sets) * scene_dur
    fade_out_start = total_dur - 0.3
    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", temp_concat,
        "-vf", f"fade=in:0:8,fade=out:st={fade_out_start}:d=0.3",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "slow",
        "-crf", "17",
        "-b:v", "15M",
        "-maxrate", "18M",
        "-bufsize", "30M",
        output
    ], "fade")

    # Cleanup
    os.remove(title_path)
    for cf in clip_files:
        os.remove(cf)
    os.remove(concat_list)
    os.remove(temp_concat)
    print(f"📱 Motion video: {output} ({os.path.getsize(output)/1024**2:.1f} MB)")

def run_ffmpeg(cmd, desc):
    print(f"⏳ {desc}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ FFmpeg error in '{desc}':\n{res.stderr}")
        raise RuntimeError(f"FFmpeg step '{desc}' failed")
    print(f"✅ {desc} done")

# ================== MAIN ==================
def main():
    ensure_waifu2x_model()
    print("🚀 Starting...")
    theme_name = random.choice(list(THEMES.keys()))
    theme = THEMES[theme_name]
    print(f"🎭 {theme_name} – {theme['title']}")

    daily_seed = random.randint(1, 100000)
    image_sets = []   # list of lists (3 images per scene)

    for i, prompt in enumerate(theme["scenes"]):
        scene_images = []
        # Generate 3 slightly different images by varying the seed
        for offset in range(3):
            seed = daily_seed + offset*10
            url = generate_fashion_images(prompt, seed=seed, width=2048, height=2730)
            resp = requests.get(url)
            if resp.status_code == 200:
                path = f"image_{i+1}_{offset+1}.jpg"
                with open(path, "wb") as f:
                    f.write(resp.content)
                upscale_with_waifu2x(path)
                scene_images.append(path)
            else:
                print(f"❌ Failed to generate image {i+1}_{offset+1}")
        if len(scene_images) == 3:
            image_sets.append(scene_images)
            print(f"✅ Scene {i+1} complete")
        else:
            print(f"⚠️ Scene {i+1} incomplete, using first image repeated")
            # Fallback: use the first image three times
            if scene_images:
                scene_images = [scene_images[0]]*3
                image_sets.append(scene_images)

    if len(image_sets) < 6:
        print("Not enough scenes.")
        return

    # Safety check (only first image of each scene)
    for scene in image_sets:
        if not is_safe(scene[0]):
            print(f"⚠️ Unsafe: {scene[0]}")
            return

    video_output = "daily_video.mp4"
    try:
        create_motion_video(image_sets, theme["title"], theme["video_style"], video_output)
    except Exception as e:
        print(f"❌ Video error: {e}")
        traceback.print_exc()
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1080x1350:d=3",
            "-c:v", "libx264", video_output
        ], check=True)

    caption = create_caption(theme["caption_context"])
    with open("caption.txt", "w") as f:
        f.write(caption)
    print(f"💬 Caption: {caption}")

if __name__ == "__main__":
    main()
