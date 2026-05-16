#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import random
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
import sys

# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------
NUMBER_OF_MEMES = 8
OUTPUT_SIZE = (1080, 1080)

# WORKING MEME TEMPLATES (all from Imgflip, verified May 2026)
# Each has: name, url, and original dimensions for coordinate scaling
MEME_TEMPLATES = {
    "drake": {
        "url": "https://i.imgflip.com/30b1gx.jpg",
        "orig_size": (1200, 675),
        "boxes": [
            {"name": "left", "orig_x": 300, "orig_y": 470, "orig_w": 500, "orig_h": 100},
            {"name": "right", "orig_x": 900, "orig_y": 470, "orig_w": 500, "orig_h": 100}
        ]
    },
    "distracted_boyfriend": {
        "url": "https://i.imgflip.com/1ur9b0.jpg",
        "orig_size": (1200, 800),
        "boxes": [
            {"name": "girlfriend", "orig_x": 220, "orig_y": 720, "orig_w": 250, "orig_h": 80},
            {"name": "boyfriend", "orig_x": 540, "orig_y": 720, "orig_w": 250, "orig_h": 80},
            {"name": "other_girl", "orig_x": 860, "orig_y": 720, "orig_w": 250, "orig_h": 80}
        ]
    },
    "two_buttons": {
        "url": "https://i.imgflip.com/1g8my4.jpg",
        "orig_size": (1200, 900),
        "boxes": [
            {"name": "left", "orig_x": 270, "orig_y": 870, "orig_w": 300, "orig_h": 80},
            {"name": "right", "orig_x": 810, "orig_y": 870, "orig_w": 300, "orig_h": 80}
        ]
    },
    "change_my_mind": {
        "url": "https://i.imgflip.com/24y43o.jpg",
        "orig_size": (1200, 800),
        "boxes": [
            {"name": "sign", "orig_x": 540, "orig_y": 540, "orig_w": 600, "orig_h": 120}
        ]
    },
    "roll_safe": {
        "url": "https://i.imgflip.com/26am.jpg",
        "orig_size": (1200, 800),
        "boxes": [
            {"name": "top", "orig_x": 540, "orig_y": 300, "orig_w": 500, "orig_h": 80},
            {"name": "bottom", "orig_x": 540, "orig_y": 700, "orig_w": 500, "orig_h": 80}
        ]
    },
    "expanding_brain": {
        "url": "https://i.imgflip.com/3lm2lk.jpg",
        "orig_size": (1200, 900),
        "boxes": [
            {"name": "level1", "orig_x": 540, "orig_y": 220, "orig_w": 400, "orig_h": 60},
            {"name": "level2", "orig_x": 540, "orig_y": 420, "orig_w": 400, "orig_h": 60},
            {"name": "level3", "orig_x": 540, "orig_y": 620, "orig_w": 400, "orig_h": 60},
            {"name": "level4", "orig_x": 540, "orig_y": 820, "orig_w": 400, "orig_h": 60}
        ]
    }
}

# ------------------------------------------------------------
# FUNNY, INDIAN-STYLE TEXT GENERATOR (no repeats)
# ------------------------------------------------------------
class TextGenerator:
    def __init__(self):
        self.used_combinations = set()
    
    def get_text(self, template, box_name, trend):
        key = f"{template}_{box_name}_{trend}"
        if key in self.used_combinations:
            # return generic fallback
            return f"{trend} be like"
        
        texts = {
            "drake_left": [
                f"Taking {trend} seriously",
                f"Listening to experts on {trend}",
                f"Mom trying to explain {trend}",
                f"News channels covering {trend}"
            ],
            "drake_right": [
                f"Making memes about {trend}",
                f"Watching {trend} reels at 2 AM",
                f"Laughing at {trend} with friends",
                f"Converting {trend} into content"
            ],
            "girlfriend": [
                "Common sense",
                "Normal people",
                "My responsibilities",
                "What I should focus on"
            ],
            "boyfriend": [
                f"Me ignoring {trend}",
                f"Me scrolling past {trend}",
                f"My brain during {trend}",
                f"Me pretending {trend} doesn't exist"
            ],
            "other_girl": [
                f"{trend} memes",
                f"Viral {trend} jokes",
                f"That one {trend} edit",
                f"{trend} reels on Insta"
            ],
            "left": [
                f"Study for exams",
                f"Sleep on time",
                f"Be productive",
                f"Respect {trend}"
            ],
            "right": [
                f"Make {trend} memes",
                f"Stay up for {trend} reels",
                f"Laugh at {trend} till 4 AM",
                f"Convert {trend} into a meme"
            ],
            "sign": [
                f"{trend} is overrated.\nChange my mind.",
                f"{trend} isn't that deep.\nI'll wait.",
                f"Y'all overreacting to {trend}.\nChange my mind.",
                f"{trend}? Really?\nChange my mind."
            ],
            "top": [
                f"Can't understand {trend}?",
                f"Confused about {trend}?",
                f"{trend} giving you headache?",
                f"Too much {trend}?"
            ],
            "bottom": [
                f"Just laugh at memes bro",
                f"Scroll and ignore",
                f"Convert it into a meme",
                f"Make a reel about it"
            ],
            "level1": [f"{trend} exists"],
            "level2": [f"People argue about {trend}"],
            "level3": [f"Memes about {trend} appear"],
            "level4": [f"{trend} becomes a legendary meme"],
        }
        
        options = texts.get(f"{template}_{box_name}", texts.get(box_name, [f"{trend} be like"]))
        chosen = random.choice(options)
        self.used_combinations.add(key)
        return chosen

# ------------------------------------------------------------
# FONT HANDLER (uses Ubuntu fonts available on GitHub runner)
# ------------------------------------------------------------
def get_font(size):
    """Get a bold font that exists on Ubuntu (GitHub Actions runner)"""
    font_paths = [
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
        "/System/Library/Fonts/Helvetica.ttc",  # macOS fallback
        "C:\\Windows\\Fonts\\Arial.ttf"         # Windows fallback
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
                # Clean and deduplicate
                unique = []
                for t in titles:
                    t = t.strip()
                    if t and len(t) > 3 and t not in unique:
                        unique.append(t)
                return unique[:20]
    except Exception as e:
        print(f"Trend fetch error: {e}")
    
    # Fallback Indian topics
    return ["IPL 2026", "Heatwave", "Bollywood Gossip", "Stock Market Crash", "Elections 2026", "Monsoon Floods", "AI News", "Cricket Match", "Delhi Pollution", "Exam Results", "Fuel Prices", "GST Council"]

# ------------------------------------------------------------
# IMAGE PROCESSING (with coordinate scaling)
# ------------------------------------------------------------
def add_text_with_outline(draw, text, x, y, font, max_width):
    """Add white text with black outline, auto-wrapped"""
    # Estimate characters per line
    try:
        char_width = font.getbbox("A")[2] - font.getbbox("A")[0]
        chars_per_line = max(10, int(max_width / char_width))
    except:
        chars_per_line = 25
    
    lines = textwrap.wrap(text, width=chars_per_line)
    if not lines:
        lines = [text]
    
    line_height = font.size + 8 if hasattr(font, 'size') else 40
    total_height = len(lines) * line_height
    start_y = y - total_height // 2
    
    for i, line in enumerate(lines):
        line_y = start_y + i * line_height
        # Draw black outline (3px stroke)
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx != 0 or dy != 0:
                    draw.text((x+dx, line_y+dy), line, fill='black', font=font, anchor='mm')
        # Draw white text
        draw.text((x, line_y), line, fill='white', font=font, anchor='mm')

def generate_meme(trend, template_name, meme_id, text_gen):
    """Generate one high-quality meme"""
    template = MEME_TEMPLATES.get(template_name)
    if not template:
        return None
    
    # Download image
    try:
        print(f"    Downloading {template_name}...")
        response = requests.get(template["url"], timeout=15)
        response.raise_for_status()
        img = Image.open(io.BytesIO(response.content))
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        # Resize to output size
        img = img.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)
        print(f"    Downloaded and resized")
    except Exception as e:
        print(f"    Download failed: {e}")
        # Fallback: create a solid color image with text (better than blank)
        img = Image.new('RGB', OUTPUT_SIZE, color='#2c3e50')
        draw = ImageDraw.Draw(img)
        fallback_font = get_font(60)
        draw.text((OUTPUT_SIZE[0]//2, OUTPUT_SIZE[1]//2), f"{trend}\nMeme unavailable", fill='white', font=fallback_font, anchor='mm')
    
    draw = ImageDraw.Draw(img)
    
    # Scale coordinates from original to new size
    orig_w, orig_h = template["orig_size"]
    scale_x = OUTPUT_SIZE[0] / orig_w
    scale_y = OUTPUT_SIZE[1] / orig_h
    
    for box in template["boxes"]:
        text = text_gen.get_text(template_name, box["name"], trend)
        # Calculate scaled position and size
        scaled_x = int(box["orig_x"] * scale_x)
        scaled_y = int(box["orig_y"] * scale_y)
        scaled_w = int(box["orig_w"] * scale_x)
        scaled_h = int(box["orig_h"] * scale_y)
        
        # Dynamic font size based on box height
        font_size = max(24, min(50, scaled_h // 2))
        font = get_font(font_size)
        
        add_text_with_outline(draw, text, scaled_x, scaled_y, font, scaled_w)
    
    # Add small watermark (not intrusive)
    try:
        small_font = get_font(20)
        date_str = datetime.now().strftime("%d %b %Y")
        draw.text((OUTPUT_SIZE[0]-130, OUTPUT_SIZE[1]-30), "@desi_meme_bot", fill='white', font=small_font)
        draw.text((30, OUTPUT_SIZE[1]-30), date_str, fill='white', font=small_font)
    except:
        pass
    
    # Save image
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"meme_{template_name}_{trend.replace(' ', '_')}_{meme_id}_{timestamp}.png"
    img.save(filename, "PNG")
    print(f"    Saved: {filename}")
    
    # Caption for social media
    caption = f"{trend} be like 😂\n\n#IndianMemes #{trend.replace(' ', '')} #Viral #Trending"
    hashtags = f"#{trend.replace(' ', '')} #{trend.replace(' ', '')}Memes #IndianMemes #ViralHumor"
    full_caption = f"{caption}\n\n{hashtags}"
    
    return {
        "image": filename,
        "caption": full_caption,
        "trend": trend,
        "template": template_name
    }

def generate_batch(count=NUMBER_OF_MEMES):
    # Get trends
    trends = get_indian_trends()
    if not trends:
        trends = ["Trending Topic"]
    print(f"📊 Found {len(trends)} Indian trends")
    
    # Shuffle and take first 'count' to avoid repeats
    random.shuffle(trends)
    selected_trends = trends[:count]
    
    # Get templates
    template_names = list(MEME_TEMPLATES.keys())
    # Shuffle templates so we don't repeat the same template in a row
    random.shuffle(template_names)
    # If we need more templates than available, repeat after shuffling again
    if count > len(template_names):
        template_names = template_names * ((count // len(template_names)) + 1)
        random.shuffle(template_names)
    selected_templates = template_names[:count]
    
    text_gen = TextGenerator()
    memes = []
    
    print(f"🎨 Generating {count} memes...")
    for i in range(count):
        trend = selected_trends[i % len(selected_trends)]
        template = selected_templates[i]
        print(f"  [{i+1}/{count}] {trend} on {template}")
        meme = generate_meme(trend, template, i+1, text_gen)
        if meme:
            memes.append(meme)
    
    # Save metadata
    with open("meme_batch_metadata.json", "w", encoding='utf-8') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "total_memes": len(memes),
            "memes": memes
        }, f, indent=2)
    
    # Save list of generated files for GitHub artifacts
    with open("generated_files.txt", "w") as f:
        for m in memes:
            f.write(m["image"] + "\n")
    
    return memes

if __name__ == "__main__":
    print("🚀 ULTIMATE MEME BOT STARTING")
    print("=" * 50)
    memes = generate_batch(NUMBER_OF_MEMES)
    print("=" * 50)
    print(f"🎉 SUCCESS! Generated {len(memes)} high-quality memes.")
