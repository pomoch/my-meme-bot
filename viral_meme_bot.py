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
OUTPUT_SIZE = (1080, 1080)  # Instagram square

# WORKING meme templates (URLs verified as of May 2026)
# Each has: name, image_url, and text areas with pixel positions
MEME_TEMPLATES = {
    "drake": {
        "url": "https://i.imgflip.com/30b1gx.jpg",
        "boxes": [
            {"name": "top", "x": 540, "y": 470, "width": 500, "height": 100},
            {"name": "bottom", "x": 540, "y": 670, "width": 500, "height": 100}
        ]
    },
    "distracted_boyfriend": {
        "url": "https://i.imgflip.com/1ur9b0.jpg",
        "boxes": [
            {"name": "girlfriend", "x": 220, "y": 720, "width": 250, "height": 80},
            {"name": "boyfriend", "x": 540, "y": 720, "width": 250, "height": 80},
            {"name": "other_girl", "x": 860, "y": 720, "width": 250, "height": 80}
        ]
    },
    "two_buttons": {
        "url": "https://i.imgflip.com/1g8my4.jpg",
        "boxes": [
            {"name": "left", "x": 270, "y": 870, "width": 300, "height": 100},
            {"name": "right", "x": 810, "y": 870, "width": 300, "height": 100}
        ]
    },
    "change_my_mind": {
        "url": "https://i.imgflip.com/24y43o.jpg",
        "boxes": [
            {"name": "sign", "x": 540, "y": 540, "width": 600, "height": 150}
        ]
    },
    "roll_safe": {
        "url": "https://i.imgflip.com/26am.jpg",
        "boxes": [
            {"name": "top", "x": 540, "y": 300, "width": 500, "height": 100},
            {"name": "bottom", "x": 540, "y": 700, "width": 500, "height": 100}
        ]
    },
    "expanding_brain": {
        "url": "https://i.imgflip.com/3lm2lk.jpg",
        "boxes": [
            {"name": "level1", "x": 540, "y": 220, "width": 400, "height": 80},
            {"name": "level2", "x": 540, "y": 420, "width": 400, "height": 80},
            {"name": "level3", "x": 540, "y": 620, "width": 400, "height": 80},
            {"name": "level4", "x": 540, "y": 820, "width": 400, "height": 80}
        ]
    },
    "unexpected_john_cena": {
        "url": "https://i.imgflip.com/1otk96.jpg",
        "boxes": [
            {"name": "top", "x": 540, "y": 120, "width": 600, "height": 100}
        ]
    }
}

# ------------------------------------------------------------
# FUNNY, SARCASTIC CAPTION GENERATOR (Indian context)
# ------------------------------------------------------------
def get_sarcastic_text(template, trend):
    """Return funny, sarcastic text for each template area"""
    funny_takes = {
        "drake_top": [
            f"Taking {trend} seriously", 
            f"Listening to experts on {trend}",
            f"Mom trying to explain {trend}"
        ],
        "drake_bottom": [
            f"Making memes about {trend}",
            f"Watching reels about {trend}",
            f"{trend} memes on Insta"
        ],
        "girlfriend": [
            f"Common sense", 
            f"Normal people", 
            f"News channels"
        ],
        "boyfriend": [
            f"Me ignoring {trend}", 
            f"Me not caring about {trend}",
            f"My brain at 3 AM"
        ],
        "other_girl": [
            f"{trend} memes", 
            f"Viral {trend} jokes",
            f"That one {trend} edit"
        ],
        "left": [
            f"Study for exams", 
            f"Sleep on time", 
            f"Respect {trend}"
        ],
        "right": [
            f"Make {trend} memes", 
            f"Stay up for {trend} reels",
            f"Laugh at {trend}"
        ],
        "sign": [
            f"{trend} is overrated.\nChange my mind.",
            f"{trend} isn't that deep.\nI'll wait.",
            f"Y'all overreacting to {trend}.\nChange my mind."
        ],
        "roll_top": [
            f"Can't understand {trend}?",
            f"Confused about {trend}?",
            f"{trend} giving you headache?"
        ],
        "roll_bottom": [
            f"Just laugh at memes bro",
            f"Scroll and ignore",
            f"Convert it into a meme"
        ],
        "level1": [f"{trend} exists"],
        "level2": [f"People argue about {trend}"],
        "level3": [f"Memes about {trend} appear"],
        "level4": [f"{trend} becomes a legendary meme"],
        "top": [f"{trend.upper()} BE LIKE...", f"WHEN {trend.upper()} HITS..."]
    }
    
    result = {}
    if template == "drake":
        result["top"] = random.choice(funny_takes["drake_top"])
        result["bottom"] = random.choice(funny_takes["drake_bottom"])
    elif template == "distracted_boyfriend":
        result["girlfriend"] = random.choice(funny_takes["girlfriend"])
        result["boyfriend"] = random.choice(funny_takes["boyfriend"])
        result["other_girl"] = random.choice(funny_takes["other_girl"])
    elif template == "two_buttons":
        result["left"] = random.choice(funny_takes["left"])
        result["right"] = random.choice(funny_takes["right"])
    elif template == "change_my_mind":
        result["sign"] = random.choice(funny_takes["sign"])
    elif template == "roll_safe":
        result["top"] = random.choice(funny_takes["roll_top"])
        result["bottom"] = random.choice(funny_takes["roll_bottom"])
    elif template == "expanding_brain":
        for i, level in enumerate(["level1","level2","level3","level4"]):
            result[level] = funny_takes[level][0] if level in funny_takes else f"Step {i+1}"
    elif template == "unexpected_john_cena":
        result["top"] = random.choice(funny_takes["top"])
    return result

# ------------------------------------------------------------
# FONT HANDLER (downloads Impact font if missing)
# ------------------------------------------------------------
def get_impact_font(size):
    """Return Impact font (classic meme font) - downloads if needed"""
    font_path = "impact.ttf"
    if not os.path.exists(font_path):
        try:
            # Download Impact font from a reliable CDN
            url = "https://github.com/google/fonts/raw/main/ofl/impact/Impact.ttf"
            r = requests.get(url, timeout=10)
            with open(font_path, "wb") as f:
                f.write(r.content)
        except:
            pass
    try:
        return ImageFont.truetype(font_path, size)
    except:
        try:
            return ImageFont.truetype("arialbd.ttf", size)
        except:
            return ImageFont.load_default()

# ------------------------------------------------------------
# TEXT DRAWING WITH OUTLINE (real meme style)
# ------------------------------------------------------------
def draw_text_with_outline(draw, text, x, y, font, max_width):
    """Draw white text with black outline, auto-wrap"""
    # Wrap text
    chars_per_line = int(max_width / (font.size * 0.6)) if font != ImageFont.load_default() else 20
    lines = textwrap.wrap(text, width=chars_per_line)
    
    # Calculate total height
    line_height = font.size + 10 if font != ImageFont.load_default() else 30
    start_y = y - (len(lines) * line_height) // 2
    
    for i, line in enumerate(lines):
        line_y = start_y + i * line_height
        # Draw black outline (3px stroke)
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx != 0 or dy != 0:
                    draw.text((x+dx, line_y+dy), line, fill='black', font=font, anchor='mm')
        # Draw white text
        draw.text((x, line_y), line, fill='white', font=font, anchor='mm')

# ------------------------------------------------------------
# TREND FETCHER
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
                return titles[:15]
    except:
        pass
    # Fallback trends (Indian context)
    return ["IPL 2026", "Heatwave", "Bollywood Gossip", "Stock Market", "Elections", "Monsoon", "AI", "Cricket", "Delhi Pollution", "Exam Results"]

# ------------------------------------------------------------
# MAIN MEME GENERATION
# ------------------------------------------------------------
def generate_meme(trend, template_name, meme_id):
    """Generate one high-quality meme"""
    template = MEME_TEMPLATES.get(template_name)
    if not template:
        return None
    
    # Download image
    try:
        response = requests.get(template["url"], timeout=15)
        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content))
            img = img.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)
        else:
            raise Exception("Failed to download")
    except Exception as e:
        print(f"Warning: Could not download {template_name}, using fallback")
        # Fallback: create gradient background
        img = Image.new('RGB', OUTPUT_SIZE, color='#1a1a2e')
        draw = ImageDraw.Draw(img)
        for i in range(OUTPUT_SIZE[1]):
            color = 30 + int(i / OUTPUT_SIZE[1] * 100)
            draw.line([(0, i), (OUTPUT_SIZE[0], i)], fill=(color, color, color+50))
    
    # Get text for this template
    texts = get_sarcastic_text(template_name, trend)
    
    # Get font (size based on box height)
    draw = ImageDraw.Draw(img)
    
    for box in template["boxes"]:
        if box["name"] not in texts:
            continue
        text = texts[box["name"]]
        # Calculate font size dynamically
        box_height = box.get("height", 100)
        font_size = min(50, max(30, box_height // 2))
        font = get_impact_font(font_size)
        
        # Draw text at box center
        draw_text_with_outline(draw, text, box["x"], box["y"], font, box["width"])
    
    # Add watermark (small, bottom right)
    try:
        small_font = get_impact_font(24)
        date_str = datetime.now().strftime("%d %b %Y")
        draw.text((OUTPUT_SIZE[0]-150, OUTPUT_SIZE[1]-40), "@daily_memes", fill='white', font=small_font)
        draw.text((50, OUTPUT_SIZE[1]-40), date_str, fill='white', font=small_font)
    except:
        pass
    
    # Save
    filename = f"viral_{template_name}_{trend.replace(' ', '_')}_{meme_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    img.save(filename, "PNG")
    print(f"✅ Saved: {filename}")
    
    # Caption and hashtags
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
    trends = get_indian_trends()
    if not trends:
        trends = ["Trending Topic"]
    
    template_names = list(MEME_TEMPLATES.keys())
    memes = []
    
    print(f"📊 Found trends: {trends[:5]}...")
    print(f"🎨 Generating {count} memes...")
    
    for i in range(count):
        trend = random.choice(trends)
        template = random.choice(template_names)
        print(f"  [{i+1}/{count}] {trend} on {template}")
        meme = generate_meme(trend, template, i+1)
        if meme:
            memes.append(meme)
    
    # Save metadata
    with open("viral_memes_metadata.json", "w", encoding='utf-8') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "total_memes": len(memes),
            "memes": memes
        }, f, indent=2)
    
    # Save file list for GitHub artifact
    with open("generated_files.txt", "w") as f:
        for m in memes:
            f.write(m["image"] + "\n")
    
    return memes

if __name__ == "__main__":
    print("🚀 VIRAL MEME BOT STARTING")
    memes = generate_batch()
    print(f"\n🎉 Done! Generated {len(memes)} memes.")
