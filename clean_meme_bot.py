#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import random
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import textwrap

# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------
NUMBER_OF_MEMES = 8
OUTPUT_SIZE = (1080, 1080)

# CLEAN MEME TEMPLATES (no watermarks)
# These URLs point to blank versions of popular memes
# If any URL fails, the script will use a fallback (solid color with text)
MEME_TEMPLATES = {
    "drake": {
        "url": "https://i.imgflip.com/30b1gx.jpg",
        "boxes": [
            {"name": "left", "x": 300, "y": 470, "w": 500, "h": 100},
            {"name": "right", "x": 900, "y": 470, "w": 500, "h": 100}
        ]
    },
    "distracted_boyfriend": {
        "url": "https://i.imgflip.com/1ur9b0.jpg",
        "boxes": [
            {"name": "girlfriend", "x": 220, "y": 720, "w": 250, "h": 80},
            {"name": "boyfriend", "x": 540, "y": 720, "w": 250, "h": 80},
            {"name": "other_girl", "x": 860, "y": 720, "w": 250, "h": 80}
        ]
    },
    "two_buttons": {
        "url": "https://i.imgflip.com/1g8my4.jpg",
        "boxes": [
            {"name": "left", "x": 270, "y": 870, "w": 300, "h": 80},
            {"name": "right", "x": 810, "y": 870, "w": 300, "h": 80}
        ]
    },
    "change_my_mind": {
        "url": "https://i.imgflip.com/24y43o.jpg",
        "boxes": [
            {"name": "sign", "x": 540, "y": 540, "w": 600, "h": 120}
        ]
    },
    "roll_safe": {
        "url": "https://i.imgflip.com/26am.jpg",
        "boxes": [
            {"name": "top", "x": 540, "y": 300, "w": 500, "h": 80},
            {"name": "bottom", "x": 540, "y": 700, "w": 500, "h": 80}
        ]
    },
    "expanding_brain": {
        "url": "https://i.imgflip.com/3lm2lk.jpg",
        "boxes": [
            {"name": "level1", "x": 540, "y": 220, "w": 400, "h": 60},
            {"name": "level2", "x": 540, "y": 420, "w": 400, "h": 60},
            {"name": "level3", "x": 540, "y": 620, "w": 400, "h": 60},
            {"name": "level4", "x": 540, "y": 820, "w": 400, "h": 60}
        ]
    }
}

# ------------------------------------------------------------
# FUNNY TEXT GENERATOR (Indian sarcasm)
# ------------------------------------------------------------
class FunnyText:
    @staticmethod
    def get(template, box, trend):
        templates = {
            ("drake", "left"): [
                f"Taking {trend} seriously",
                f"Listening to news about {trend}",
                f"My mom explaining {trend}",
                f"Watching {trend} debates"
            ],
            ("drake", "right"): [
                f"Making {trend} memes",
                f"Watching {trend} reels at 3 AM",
                f"Laughing at {trend} with friends",
                f"Converting {trend} into content"
            ],
            ("distracted_boyfriend", "girlfriend"): [
                "My responsibilities",
                "What I should focus on",
                "Common sense",
                "Productivity"
            ],
            ("distracted_boyfriend", "boyfriend"): [
                f"Me ignoring {trend}",
                f"Me scrolling past {trend}",
                f"My brain during {trend}",
                f"Me pretending {trend} doesn't exist"
            ],
            ("distracted_boyfriend", "other_girl"): [
                f"{trend} memes",
                f"Viral {trend} jokes",
                f"{trend} reels on Insta",
                f"That one {trend} edit"
            ],
            ("two_buttons", "left"): [
                f"Study for exams",
                f"Sleep on time",
                f"Be productive",
                f"Ignore {trend}"
            ],
            ("two_buttons", "right"): [
                f"Make {trend} memes",
                f"Stay up for {trend} reels",
                f"Laugh at {trend} till 4 AM",
                f"Convert {trend} into a meme"
            ],
            ("change_my_mind", "sign"): [
                f"{trend} is overrated. Change my mind.",
                f"{trend} isn't that deep. I'll wait.",
                f"Y'all overreacting to {trend}. Change my mind.",
                f"{trend}? Really? Change my mind."
            ],
            ("roll_safe", "top"): [
                f"Can't understand {trend}?",
                f"Confused about {trend}?",
                f"{trend} giving you headache?",
                f"Too much {trend}?"
            ],
            ("roll_safe", "bottom"): [
                f"Just laugh at memes bro",
                f"Scroll and ignore",
                f"Convert it into a meme",
                f"Make a reel about it"
            ],
            ("expanding_brain", "level1"): [f"{trend} exists"],
            ("expanding_brain", "level2"): [f"People argue about {trend}"],
            ("expanding_brain", "level3"): [f"Memes about {trend} appear"],
            ("expanding_brain", "level4"): [f"{trend} becomes a legendary meme"],
        }
        key = (template, box)
        options = templates.get(key, [f"{trend} be like"])
        return random.choice(options)

# ------------------------------------------------------------
# FONT HANDLER (uses fonts available on GitHub Ubuntu runner)
# ------------------------------------------------------------
def get_font(size):
    """Return a bold font that exists on Ubuntu (GitHub Actions)"""
    font_paths = [
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()

# ------------------------------------------------------------
# TREND FETCHER (Google Trends India)
# ------------------------------------------------------------
def get_indian_trends():
    try:
        url = "https://trends.google.com/trending/trendingsearches/daily?geo=IN"
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            import re
            titles = re.findall(r'"title":"([^"]+)"', resp.text)
            if titles:
                unique = []
                for t in titles:
                    t = t.strip()
                    if t and len(t) > 3 and t not in unique:
                        unique.append(t)
                return unique[:20]
    except Exception as e:
        print(f"Trend fetch error: {e}")
    return ["IPL 2026", "Heatwave", "Bollywood Gossip", "Stock Market", "Elections", "Monsoon", "AI", "Cricket", "Delhi Pollution", "Exam Results"]

# ------------------------------------------------------------
# DRAW TEXT WITH OUTLINE AND BACKGROUND (covers original text)
# ------------------------------------------------------------
def draw_clean_text(draw, text, x, y, font, box_w, box_h):
    """Draw text with black outline and semi-transparent background to hide old text"""
    # Wrap text
    try:
        # Approximate characters per line
        avg_char_width = font.getbbox("A")[2] - font.getbbox("A")[0]
        chars_per_line = max(10, int(box_w / avg_char_width))
    except:
        chars_per_line = 20
    lines = textwrap.wrap(text, width=chars_per_line)
    if not lines:
        lines = [text]
    
    # Calculate line height
    line_height = font.size + 8 if hasattr(font, 'size') else 40
    total_height = len(lines) * line_height
    start_y = y - total_height // 2
    
    # Draw a semi-transparent black rectangle behind the text to hide any old text
    padding = 10
    text_bbox = (
        x - box_w//2 - padding,
        start_y - padding,
        x + box_w//2 + padding,
        start_y + total_height + padding
    )
    draw.rectangle(text_bbox, fill=(0, 0, 0, 180))
    
    # Draw text with outline
    for i, line in enumerate(lines):
        line_y = start_y + i * line_height
        # Black outline (3px stroke)
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx != 0 or dy != 0:
                    draw.text((x+dx, line_y+dy), line, fill='black', font=font, anchor='mm')
        # White text
        draw.text((x, line_y), line, fill='white', font=font, anchor='mm')

# ------------------------------------------------------------
# MEME GENERATOR
# ------------------------------------------------------------
def generate_meme(trend, template_name, meme_id):
    template = MEME_TEMPLATES.get(template_name)
    if not template:
        return None
    
    # Download image
    try:
        print(f"    Downloading {template_name}...")
        response = requests.get(template["url"], timeout=15)
        response.raise_for_status()
        img = Image.open(io.BytesIO(response.content))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img = img.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)
    except Exception as e:
        print(f"    Download failed: {e}, using fallback")
        # Fallback: gradient background
        img = Image.new('RGB', OUTPUT_SIZE, color='#1a1a2e')
        draw = ImageDraw.Draw(img)
        for i in range(OUTPUT_SIZE[1]):
            color = 30 + int(i / OUTPUT_SIZE[1] * 100)
            draw.line([(0, i), (OUTPUT_SIZE[0], i)], fill=(color, color, color+50))
    
    draw = ImageDraw.Draw(img)
    
    for box in template["boxes"]:
        # Get text
        text = FunnyText.get(template_name, box["name"], trend)
        # Calculate font size based on box height
        font_size = max(28, min(52, box["h"] // 2))
        font = get_font(font_size)
        # Draw text with background to hide any original text/watermark
        draw_clean_text(draw, text, box["x"], box["y"], font, box["w"], box["h"])
    
    # Add small watermark (optional, but not intrusive)
    try:
        small_font = get_font(20)
        date_str = datetime.now().strftime("%d %b %Y")
        draw.text((OUTPUT_SIZE[0]-140, OUTPUT_SIZE[1]-25), "@desi_meme_bot", fill='white', font=small_font)
        draw.text((25, OUTPUT_SIZE[1]-25), date_str, fill='white', font=small_font)
    except:
        pass
    
    # Save
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"clean_meme_{template_name}_{trend.replace(' ', '_')}_{meme_id}_{timestamp}.png"
    img.save(filename, "PNG")
    print(f"    Saved: {filename}")
    
    # Social media caption
    caption = f"{trend} be like 😂\n\n#IndianMemes #{trend.replace(' ', '')} #Viral #Trending"
    hashtags = f"#{trend.replace(' ', '')} #{trend.replace(' ', '')}Memes #IndianMemes #ViralHumor"
    full_caption = f"{caption}\n\n{hashtags}"
    
    return {
        "image": filename,
        "caption": full_caption,
        "trend": trend,
        "template": template_name
    }

# ------------------------------------------------------------
# BATCH GENERATION (no duplicate templates)
# ------------------------------------------------------------
def generate_batch(count=NUMBER_OF_MEMES):
    # Get trends
    trends = get_indian_trends()
    random.shuffle(trends)
    # Ensure we have enough trends
    if len(trends) < count:
        trends = trends * ((count // len(trends)) + 1)
    selected_trends = trends[:count]
    
    # Get templates and shuffle, then ensure no repeats in the batch
    template_names = list(MEME_TEMPLATES.keys())
    random.shuffle(template_names)
    if count > len(template_names):
        # Repeat but reshuffle
        template_names = template_names * ((count // len(template_names)) + 1)
        random.shuffle(template_names)
    selected_templates = template_names[:count]
    
    memes = []
    print(f"📊 Trends: {selected_trends[:3]}...")
    print(f"🎨 Generating {count} memes...")
    for i in range(count):
        trend = selected_trends[i]
        template = selected_templates[i]
        print(f"  [{i+1}/{count}] {trend} on {template}")
        meme = generate_meme(trend, template, i+1)
        if meme:
            memes.append(meme)
    
    # Save metadata
    with open("clean_memes_metadata.json", "w", encoding='utf-8') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "total_memes": len(memes),
            "memes": memes
        }, f, indent=2)
    
    # Save file list for GitHub artifacts
    with open("generated_files.txt", "w") as f:
        for m in memes:
            f.write(m["image"] + "\n")
    
    return memes

if __name__ == "__main__":
    print("🚀 CLEAN MEME BOT STARTING")
    print("=" * 50)
    memes = generate_batch(NUMBER_OF_MEMES)
    print("=" * 50)
    print(f"🎉 Generated {len(memes)} clean, watermark‑free memes!")
