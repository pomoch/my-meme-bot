import os
import requests
import random
from PIL import Image, ImageFilter
from generate_image import generate_fashion_images
from generate_video import create_themed_video
from generate_caption import create_caption
from safety_check import is_safe

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

def sharpen_image(path):
    """Apply unsharp mask to make the image look like it was shot on a premium camera."""
    try:
        img = Image.open(path).convert("RGB")
        sharpened = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=0))
        sharpened.save(path, quality=95)
        print(f"🔪 Sharpened {path}")
    except Exception as e:
        print(f"⚠️ Could not sharpen {path}: {e}")

def main():
    print("🚀 Starting daily influencer content generation...")

    # 1. Randomly pick a theme
    theme_name = random.choice(list(THEMES.keys()))
    theme = THEMES[theme_name]
    print(f"🎭 Today's theme: {theme_name} ({theme['title']})")

    # Fixed seed for character consistency today
    daily_seed = random.randint(1, 100000)

    # 2. Generate all 6 images
    image_paths = []
    for i, scene_prompt in enumerate(theme["scenes"]):
        url = generate_fashion_images(
            scene_prompt, seed=daily_seed,
            width=1080, height=1350
        )
        resp = requests.get(url)
        if resp.status_code == 200:
            path = f"image_{i+1}.jpg"
            with open(path, "wb") as f:
                f.write(resp.content)
            sharpen_image(path)  # <-- sharpen after save
            image_paths.append(path)
            print(f"✅ Image {i+1} generated and sharpened")
        else:
            print(f"❌ Failed to generate image {i+1}")

    if len(image_paths) < 6:
        print("Not enough images, aborting.")
        return

    # 3. Safety check
    for img in image_paths:
        if not is_safe(img):
            print(f"⚠️ Unsafe content in {img}, aborting.")
            return

    # 4. Create video with theme-specific style
    video_path = create_themed_video(
        image_paths,
        title_text=theme["title"],
        video_style=theme["video_style"],
        wiggle=theme["wiggle"],
        output="daily_video.mp4"
    )
    print(f"🎬 Video created: {video_path}")

    # 5. Generate caption
    caption = create_caption(theme["caption_context"])
    with open("caption.txt", "w") as f:
        f.write(caption)
    print(f"💬 Caption: {caption}")

    print("📦 Content ready for email delivery.")

if __name__ == "__main__":
    main()
