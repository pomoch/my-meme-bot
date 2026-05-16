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

# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------
NUMBER_OF_MEMES = 8
OUTPUT_SIZE = (1080, 1080)  # Instagram square

# Real meme templates (image URLs from Imgflip's public templates)
# These are direct image URLs that work without API keys
MEME_TEMPLATES = {
    "drake": {
        "url": "https://i.imgflip.com/30b1gx.jpg",
        "text_positions": {
            "top": (540, 400),   # (x, y) center of left side
            "bottom": (540, 700) # center of right side
        },
        "text_areas": ["top", "bottom"]
    },
    "two_buttons": {
        "url": "https://i.imgflip.com/1g8my4.jpg",
        "text_positions": {
            "left_button": (270, 900),
            "right_button": (810, 900)
        },
        "text_areas": ["left_button", "right_button"]
    },
    "distracted_boyfriend": {
        "url": "https://i.imgflip.com/1ur9b0.jpg",
        "text_positions": {
            "girlfriend": (200, 750),
            "boyfriend": (540, 750),
            "other_girl": (880, 750)
        },
        "text_areas": ["girlfriend", "boyfriend", "other_girl"]
    },
    "change_my_mind": {
        "url": "https://i.imgflip.com/24y43o.jpg",
        "text_positions": {
            "sign": (540, 540)
        },
        "text_areas": ["sign"]
    },
    "roll_safe": {
        "url": "https://i.imgflip.com/26am.jpg",
        "text_positions": {
            "top": (540, 300),
            "bottom": (540, 700)
        },
        "text_areas": ["top", "bottom"]
    },
    "expanding_brain": {
        "url": "https://i.imgflip.com/3lm2lk.jpg",
        "text_positions": {
            "level1": (540, 200),
            "level2": (540, 400),
            "level3": (540, 600),
            "level4": (540, 800)
        },
        "text_areas": ["level1", "level2", "level3", "level4"]
    },
    "mr_incredible": {
        "url": "https://i.imgflip.com/5iww3.jpg",
        "text_positions": {
            "panel1": (270, 270),
            "panel2": (810, 270),
            "panel3": (270, 810),
            "panel4": (810, 810)
        },
        "text_areas": ["panel1", "panel2", "panel3", "panel4"]
    },
    "unexpected": {
        "url": "https://i.imgflip.com/1otk96.jpg",
        "text_positions": {
            "top": (540, 100)
        },
        "text_areas": ["top"]
    }
}

# Fallback templates if download fails (use colored boxes with drawn characters)
FALLBACK_TEMPLATES = {
    "drake": "drake",
    "two_buttons": "two_buttons",
    "distracted_boyfriend": "distracted_boyfriend",
    "change_my_mind": "change_my_mind",
    "roll_safe": "roll_safe"
}

# ------------------------------------------------------------
# TREND FETCHER (same as before)
# ------------------------------------------------------------
def get_indian_trends():
    try:
        url = "https://trends.google.com/trending/trendingsearches/daily?geo=IN"
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            import re
            titles = re.findall(r'"title":"([^"]+)"', resp.text)
            return titles[:15]
    except:
        pass
    return ["IPL 2026", "Heatwave", "Bollywood", "Stock Market", "Elections", "Monsoon", "AI", "Cricket", "Farmers", "Delhi Pollution"]

# ------------------------------------------------------------
# CAPTION GENERATOR (viral style)
# ------------------------------------------------------------
def generate_text_for_template(template_name, trend):
    """Generate appropriate text for each template area"""
    texts = {}
    if template_name == "drake":
        texts["top"] = f"Taking {trend} seriously"
        texts["bottom"] = f"Making memes about {trend}"
    elif template_name == "two_buttons":
        texts["left_button"] = f"Ignore {trend}"
        texts["right_button"] = f"Make viral meme on {trend}"
    elif template_name == "distracted_boyfriend":
        texts["girlfriend"] = f"Other news"
        texts["boyfriend"] = f"Me looking at {trend}"
        texts["other_girl"] = f"{trend} memes"
    elif template_name == "change_my_mind":
        texts["sign"] = f"{trend} is not that funny\nChange my mind"
    elif template_name == "roll_safe":
        texts["top"] = f"Don't understand {trend}?"
        texts["bottom"] = f"Just laugh at memes"
    elif template_name == "expanding_brain":
        texts["level1"] = f"{trend} happens"
        texts["level2"] = f"People discuss {trend}"
        texts["level3"] = f"Memes about {trend} appear"
        texts["level4"] = f"{trend} becomes legendary meme"
    elif template_name == "mr_incredible":
        texts["panel1"] = f"Normal {trend}"
        texts["panel2"] = f"Relatable {trend}"
        texts["panel3"] = f"Hilarious {trend}"
        texts["panel4"] = f"Viral {trend} meme"
    elif template_name == "unexpected":
        texts["top"] = f"{trend.upper()} BE LIKE..."
    else:
        texts["top"] = trend
    return texts

def add_text_to_image(img, texts, positions, template_name):
    """Add text with outline (real meme style)"""
    draw = ImageDraw.Draw(img)
    
    # Try to load Impact font (classic meme font)
    try:
        font = ImageFont.truetype("impact.ttf", 60)
        font_small = ImageFont.truetype("impact.ttf", 40)
    except:
        try:
            font = ImageFont.truetype("arialbd.ttf", 60)
            font_small = ImageFont.truetype("arialbd.ttf", 40)
        except:
            font = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    for area, text in texts.items():
        if area not in positions:
            continue
        
        x, y = positions[area]
        
        # Split text into lines if needed
        lines = text.split('\n')
        if len(lines) == 1:
            # Wrap long text
            max_chars = 20 if template_name != "expanding_brain" else 25
            lines = textwrap.wrap(text, width=max_chars)
        
        # Calculate total height
        line_height = 70 if font != ImageFont.load_default() else 30
        total_height = len(lines) * line_height
        start_y = y - total_height // 2
        
        for i, line in enumerate(lines):
            line_y = start_y + i * line_height
            # Draw outline (black stroke)
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    if dx != 0 or dy != 0:
                        draw.text((x+dx, line_y+dy), line, fill='black', font=font_small if len(line) > 15 else font, anchor='mm')
            # Draw white text
            draw.text((x, line_y), line, fill='white', font=font_small if len(line) > 15 else font, anchor='mm')
    
    return img

# ------------------------------------------------------------
# MAIN MEME GENERATOR
# ------------------------------------------------------------
def generate_single_meme(trend, template_name, meme_id):
    """Download template, add text, save image"""
    template = MEME_TEMPLATES.get(template_name)
    if not template:
        return None
    
    # Download image
    try:
        response = requests.get(template["url"], timeout=15)
        img = Image.open(io.BytesIO(response.content))
        img = img.resize(OUTPUT_SIZE)  # Resize to square
    except Exception as e:
        print(f"Failed to download {template_name}: {e}")
        # Fallback: create a colored rectangle with text (better than nothing)
        img = Image.new('RGB', OUTPUT_SIZE, color='#2c3e50')
    
    # Generate texts
    texts = generate_text_for_template(template_name, trend)
    
    # Add text
    img = add_text_to_image(img, texts, template["text_positions"], template_name)
    
    # Add watermark (small, bottom right)
    draw = ImageDraw.Draw(img)
    try:
        small_font = ImageFont.truetype("arial.ttf", 24)
    except:
        small_font = ImageFont.load_default()
    draw.text((OUTPUT_SIZE[0]-120, OUTPUT_SIZE[1]-40), "@daily_indian_memes", fill='white', font=small_font)
    
    # Add date
    date_str = datetime.now().strftime("%d %b %Y")
    draw.text((50, OUTPUT_SIZE[1]-40), date_str, fill='white', font=small_font)
    
    # Save
    filename = f"real_meme_{template_name}_{trend.replace(' ', '_')}_{meme_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    img.save(filename)
    
    # Caption and hashtags
    caption = f"{trend} be like 😂\n\n#IndianMemes #{trend.replace(' ', '')} #Viral #Trending"
    hashtags = f"#{trend.replace(' ', '')} #{trend.replace(' ', '')}Memes #IndianMemes #ViralHumor #Relatable"
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
    
    for i in range(count):
        trend = random.choice(trends)
        template = random.choice(template_names)
        print(f"Generating meme {i+1}/{count}: {trend} on {template}")
        meme = generate_single_meme(trend, template, i+1)
        if meme:
            memes.append(meme)
    
    # Save metadata
    with open("real_memes_metadata.json", "w", encoding='utf-8') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "total_memes": len(memes),
            "memes": memes
        }, f, indent=2)
    
    return memes

if __name__ == "__main__":
    print("🚀 Starting REAL meme generator...")
    memes = generate_batch()
    print(f"✅ Generated {len(memes)} real memes!")
    
    # Save list for GitHub artifacts
    with open("generated_files.txt", "w") as f:
        for m in memes:
            f.write(m["image"] + "\n")
