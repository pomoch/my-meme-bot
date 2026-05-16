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
# CONFIG
# ------------------------------------------------------------
NUMBER_OF_MEMES = 8
OUTPUT_SIZE = (1080, 1080)

# MODERN MEME TEMPLATES (all working, no watermarks)
# Format: name, url, and text boxes with ORIGINAL coordinates (from the raw image)
MEME_TEMPLATES = {
    "drake": {
        "url": "https://i.imgflip.com/30b1gx.jpg",
        "boxes": [{"name": "left", "x": 300, "y": 470, "w": 500, "h": 100},
                  {"name": "right", "x": 900, "y": 470, "w": 500, "h": 100}]
    },
    "distracted_boyfriend": {
        "url": "https://i.imgflip.com/1ur9b0.jpg",
        "boxes": [{"name": "girlfriend", "x": 220, "y": 720, "w": 250, "h": 80},
                  {"name": "boyfriend", "x": 540, "y": 720, "w": 250, "h": 80},
                  {"name": "other_girl", "x": 860, "y": 720, "w": 250, "h": 80}]
    },
    "two_buttons": {
        "url": "https://i.imgflip.com/1g8my4.jpg",
        "boxes": [{"name": "left", "x": 270, "y": 870, "w": 300, "h": 80},
                  {"name": "right", "x": 810, "y": 870, "w": 300, "h": 80}]
    },
    "change_my_mind": {
        "url": "https://i.imgflip.com/24y43o.jpg",
        "boxes": [{"name": "sign", "x": 540, "y": 540, "w": 600, "h": 120}]
    },
    "roll_safe": {
        "url": "https://i.imgflip.com/26am.jpg",
        "boxes": [{"name": "top", "x": 540, "y": 300, "w": 500, "h": 80},
                  {"name": "bottom", "x": 540, "y": 700, "w": 500, "h": 80}]
    },
    "expanding_brain": {
        "url": "https://i.imgflip.com/3lm2lk.jpg",
        "boxes": [{"name": "level1", "x": 540, "y": 220, "w": 400, "h": 60},
                  {"name": "level2", "x": 540, "y": 420, "w": 400, "h": 60},
                  {"name": "level3", "x": 540, "y": 620, "w": 400, "h": 60},
                  {"name": "level4", "x": 540, "y": 820, "w": 400, "h": 60}]
    },
    # NEW MODERN TEMPLATES (2024-2026 viral)
    "woman_yelling_at_cat": {
        "url": "https://i.imgflip.com/3si4.jpg",
        "boxes": [{"name": "woman", "x": 300, "y": 450, "w": 400, "h": 100},
                  {"name": "cat", "x": 900, "y": 450, "w": 400, "h": 100}]
    },
    "trumpet_boy": {
        "url": "https://i.imgflip.com/2kbnqp.jpg",
        "boxes": [{"name": "text", "x": 540, "y": 600, "w": 600, "h": 100}]
    },
    "giga_chad": {
        "url": "https://i.imgflip.com/3lm2lk.jpg",  # placeholder - will replace
        "boxes": [{"name": "top", "x": 540, "y": 200, "w": 500, "h": 80},
                  {"name": "bottom", "x": 540, "y": 700, "w": 500, "h": 80}]
    },
    "elon_musk_meme": {
        "url": "https://i.imgflip.com/5iww3.jpg",
        "boxes": [{"name": "text", "x": 540, "y": 540, "w": 600, "h": 100}]
    },
    "crying_whitney": {
        "url": "https://i.imgflip.com/1h8n4t.jpg",
        "boxes": [{"name": "text", "x": 540, "y": 720, "w": 600, "h": 80}]
    }
}

# ------------------------------------------------------------
# TREND CATEGORY DETECTION (to pick the right template)
# ------------------------------------------------------------
def categorize_trend(trend):
    trend_lower = trend.lower()
    if any(word in trend_lower for word in ["pollution", "heatwave", "monsoon", "flood", "weather"]):
        return "serious"
    if any(word in trend_lower for word in ["cricket", "ipl", "sports", "match"]):
        return "sports"
    if any(word in trend_lower for word in ["election", "modi", "bjp", "congress", "political"]):
        return "political"
    if any(word in trend_lower for word in ["movie", "bollywood", "actor", "film"]):
        return "bollywood"
    if any(word in trend_lower for word in ["stock", "market", "gst", "economy"]):
        return "finance"
    return "funny"

# Map category to preferred templates (order matters)
TEMPLATE_PREFERENCE = {
    "serious": ["change_my_mind", "roll_safe", "expanding_brain"],
    "sports": ["drake", "two_buttons", "trumpet_boy"],
    "political": ["change_my_mind", "woman_yelling_at_cat", "crying_whitney"],
    "bollywood": ["distracted_boyfriend", "two_buttons", "drake"],
    "finance": ["roll_safe", "giga_chad", "expanding_brain"],
    "funny": ["drake", "distracted_boyfriend", "woman_yelling_at_cat", "trumpet_boy"]
}

# ------------------------------------------------------------
# TEXT GENERATOR (funny & sarcastic)
# ------------------------------------------------------------
def get_meme_text(template_name, box_name, trend):
    """Returns text based on template and trend"""
    templates = {
        ("drake", "left"): [f"Taking {trend} seriously", f"News channels on {trend}"],
        ("drake", "right"): [f"Making {trend} memes", f"Watching {trend} reels at 3 AM"],
        ("distracted_boyfriend", "girlfriend"): ["My responsibilities", "Common sense"],
        ("distracted_boyfriend", "boyfriend"): [f"Me ignoring {trend}", f"Me scrolling past {trend}"],
        ("distracted_boyfriend", "other_girl"): [f"{trend} memes", f"Viral {trend} jokes"],
        ("two_buttons", "left"): [f"Study for exams", f"Be productive"],
        ("two_buttons", "right"): [f"Make {trend} memes", f"Stay up for {trend} reels"],
        ("change_my_mind", "sign"): [f"{trend} is overrated. Change my mind."],
        ("roll_safe", "top"): [f"Can't understand {trend}?", f"Confused about {trend}?"],
        ("roll_safe", "bottom"): [f"Just laugh at memes", f"Scroll and ignore"],
        ("expanding_brain", "level1"): [f"{trend} exists"],
        ("expanding_brain", "level2"): [f"People argue about {trend}"],
        ("expanding_brain", "level3"): [f"Memes about {trend} appear"],
        ("expanding_brain", "level4"): [f"{trend} becomes a legendary meme"],
        ("woman_yelling_at_cat", "woman"): [f"Me arguing about {trend}", f"News channels on {trend}"],
        ("woman_yelling_at_cat", "cat"): [f"{trend} memes", f"Me ignoring {trend}"],
        ("trumpet_boy", "text"): [f"{trend} be like... \n*trumpet noises*"],
        ("crying_whitney", "text"): [f"Me when I see {trend} trending", f"Reaction to {trend}"]
    }
    key = (template_name, box_name)
    options = templates.get(key, [f"{trend} be like"])
    return random.choice(options)

# ------------------------------------------------------------
# FONT (Ubuntu runner)
# ------------------------------------------------------------
def get_font(size):
    paths = ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

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
            return list(dict.fromkeys(titles[:20]))  # unique
    except:
        pass
    return ["IPL 2026", "Heatwave", "Bollywood", "Stock Market", "Elections", "Monsoon", "AI", "Cricket", "Delhi Pollution", "Exam Results"]

# ------------------------------------------------------------
# DRAW TEXT WITH BACKGROUND (hides original)
# ------------------------------------------------------------
def draw_clean_text(draw, text, x, y, font, box_w, box_h):
    lines = textwrap.wrap(text, width=max(10, int(box_w / (font.size * 0.6)))) if hasattr(font, 'size') else [text]
    line_h = font.size + 8 if hasattr(font, 'size') else 40
    total_h = len(lines) * line_h
    start_y = y - total_h // 2
    # Dark background to hide old text
    pad = 10
    draw.rectangle([x - box_w//2 - pad, start_y - pad, x + box_w//2 + pad, start_y + total_h + pad], fill=(0,0,0,200))
    for i, line in enumerate(lines):
        line_y = start_y + i * line_h
        for dx in range(-3,4):
            for dy in range(-3,4):
                if dx!=0 or dy!=0:
                    draw.text((x+dx, line_y+dy), line, fill='black', font=font, anchor='mm')
        draw.text((x, line_y), line, fill='white', font=font, anchor='mm')

# ------------------------------------------------------------
# MEME GENERATION (with scaling)
# ------------------------------------------------------------
def generate_meme(trend, template_name, meme_id):
    template = MEME_TEMPLATES.get(template_name)
    if not template:
        return None
    # Download
    try:
        resp = requests.get(template["url"], timeout=15)
        resp.raise_for_status()
        img = Image.open(io.BytesIO(resp.content)).convert('RGB')
    except:
        img = Image.new('RGB', OUTPUT_SIZE, (30,30,50))
    # Get original size
    orig_w, orig_h = img.size
    # Resize to OUTPUT_SIZE
    img = img.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)
    scale_x = OUTPUT_SIZE[0] / orig_w
    scale_y = OUTPUT_SIZE[1] / orig_h
    draw = ImageDraw.Draw(img)
    
    for box in template["boxes"]:
        text = get_meme_text(template_name, box["name"], trend)
        # Scale coordinates
        scaled_x = int(box["x"] * scale_x)
        scaled_y = int(box["y"] * scale_y)
        scaled_w = int(box["w"] * scale_x)
        scaled_h = int(box["h"] * scale_y)
        font_size = max(28, min(52, scaled_h // 2))
        font = get_font(font_size)
        draw_clean_text(draw, text, scaled_x, scaled_y, font, scaled_w, scaled_h)
    
    # Watermark (small)
    try:
        small_font = get_font(20)
        date = datetime.now().strftime("%d %b %Y")
        draw.text((OUTPUT_SIZE[0]-130, OUTPUT_SIZE[1]-25), "@desi_meme_bot", fill='white', font=small_font)
        draw.text((25, OUTPUT_SIZE[1]-25), date, fill='white', font=small_font)
    except:
        pass
    
    fname = f"smart_meme_{template_name}_{trend.replace(' ', '_')}_{meme_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    img.save(fname)
    return {"image": fname, "caption": f"{trend} be like 😂\n\n#IndianMemes #{trend.replace(' ', '')} #Viral", "trend": trend, "template": template_name}

# ------------------------------------------------------------
# BATCH GENERATION (no duplicate templates)
# ------------------------------------------------------------
def generate_batch(count=NUMBER_OF_MEMES):
    trends = get_indian_trends()
    random.shuffle(trends)
    if len(trends) < count:
        trends = (trends * (count//len(trends)+1))[:count]
    selected_trends = trends[:count]
    
    # For each trend, pick a template based on its category, ensuring no repeats
    used_templates = set()
    memes = []
    for trend in selected_trends:
        category = categorize_trend(trend)
        candidates = TEMPLATE_PREFERENCE.get(category, TEMPLATE_PREFERENCE["funny"])
        # Pick first candidate not used, else fallback
        chosen = None
        for cand in candidates:
            if cand not in used_templates:
                chosen = cand
                break
        if not chosen:
            # All templates used? Reset used set (unlikely)
            used_templates.clear()
            chosen = candidates[0]
        used_templates.add(chosen)
        meme = generate_meme(trend, chosen, len(memes)+1)
        if meme:
            memes.append(meme)
    
    # Save metadata
    with open("smart_memes_metadata.json", "w") as f:
        json.dump({"generated_at": datetime.now().isoformat(), "total_memes": len(memes), "memes": memes}, f, indent=2)
    with open("generated_files.txt", "w") as f:
        for m in memes:
            f.write(m["image"] + "\n")
    return memes

if __name__ == "__main__":
    print("🚀 SMART MEME BOT")
    memes = generate_batch(NUMBER_OF_MEMES)
    print(f"✅ Generated {len(memes)} memes")
