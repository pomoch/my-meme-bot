#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import random
import requests
import textwrap
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import base64
import time

# ------------------------------------------------------------
#  CONFIGURATION (change these to your liking)
# ------------------------------------------------------------
NUMBER_OF_MEMES = 8               # memes per run
OUTPUT_SIZE = (1080, 1080)        # Instagram square format
BACKGROUND_COLORS = ['#1a1a2e', '#16213e', '#0f3460', '#533483', '#e94560', '#f5f5dc', '#ffe4e1']
FALLBACK_TRENDS = [
    "IPL 2026", "Heatwave India", "Bollywood Gossip", "Stock Market Crash",
    "Board Results", "Monsoon Floods", "New OTT Release", "Fuel Price Hike",
    "GST Council Meet", "RBI Decision", "Farmers Protest", "Delhi Pollution",
    "Bangalore Traffic", "Mumbai Local", "Wedding Season", "TikTok Ban",
    "AI News", "Space Launch", "Cricket World Cup", "Indian Elections"
]

# ------------------------------------------------------------
#  VIRAL MEME TEMPLATES (each has a drawing function)
# ------------------------------------------------------------
class MemeTemplates:
    @staticmethod
    def drake(img, draw, top_text, bottom_text, font_large, font_small):
        """Drake hotline bling template"""
        # left side (disapproving)
        draw.rectangle([0, 0, OUTPUT_SIZE[0]//2, OUTPUT_SIZE[1]], fill='#2c3e50')
        # right side (approving)
        draw.rectangle([OUTPUT_SIZE[0]//2, 0, OUTPUT_SIZE[0], OUTPUT_SIZE[1]], fill='#34495e')
        draw.text((OUTPUT_SIZE[0]//4, OUTPUT_SIZE[1]//2), top_text, fill='white', font=font_small, anchor='mm')
        draw.text((3*OUTPUT_SIZE[0]//4, OUTPUT_SIZE[1]//2), bottom_text, fill='white', font=font_small, anchor='mm')
        return img

    @staticmethod
    def two_buttons(img, draw, left_text, right_text, font_small):
        """Two buttons (choose wisely)"""
        draw.rectangle([0, OUTPUT_SIZE[1]-150, OUTPUT_SIZE[0]//2, OUTPUT_SIZE[1]], fill='#2980b9')
        draw.rectangle([OUTPUT_SIZE[0]//2, OUTPUT_SIZE[1]-150, OUTPUT_SIZE[0], OUTPUT_SIZE[1]], fill='#c0392b')
        draw.text((OUTPUT_SIZE[0]//4, OUTPUT_SIZE[1]-75), left_text, fill='white', font=font_small, anchor='mm')
        draw.text((3*OUTPUT_SIZE[0]//4, OUTPUT_SIZE[1]-75), right_text, fill='white', font=font_small, anchor='mm')
        return img

    @staticmethod
    def distracted_boyfriend(img, draw, girl_text, new_girl_text, guy_text, font_small):
        """Distracted boyfriend"""
        # Simple version: three sections
        draw.rectangle([0, 0, OUTPUT_SIZE[0]//3, OUTPUT_SIZE[1]], fill='#e74c3c')
        draw.rectangle([OUTPUT_SIZE[0]//3, 0, 2*OUTPUT_SIZE[0]//3, OUTPUT_SIZE[1]], fill='#ecf0f1')
        draw.rectangle([2*OUTPUT_SIZE[0]//3, 0, OUTPUT_SIZE[0], OUTPUT_SIZE[1]], fill='#3498db')
        draw.text((OUTPUT_SIZE[0]//6, OUTPUT_SIZE[1]//2), girl_text, fill='white', font=font_small, anchor='mm')
        draw.text((OUTPUT_SIZE[0]//2, OUTPUT_SIZE[1]//2), guy_text, fill='black', font=font_small, anchor='mm')
        draw.text((5*OUTPUT_SIZE[0]//6, OUTPUT_SIZE[1]//2), new_girl_text, fill='white', font=font_small, anchor='mm')
        return img

    @staticmethod
    def change_my_mind(img, draw, bottom_text, font_large):
        """Change my mind (old man at desk)"""
        img = Image.new('RGB', OUTPUT_SIZE, color='#f39c12')
        draw = ImageDraw.Draw(img)
        # Draw a simple desk
        draw.rectangle([0, OUTPUT_SIZE[1]-200, OUTPUT_SIZE[0], OUTPUT_SIZE[1]], fill='#8e44ad')
        draw.text((OUTPUT_SIZE[0]//2, OUTPUT_SIZE[1]//2), bottom_text, fill='black', font=font_large, anchor='mm')
        return img

    @staticmethod
    def expanding_brain(img, draw, text_levels, font_small):
        """Expanding brain (4 levels)"""
        levels = len(text_levels)
        height_per = OUTPUT_SIZE[1] // levels
        colors = ['#7f8c8d', '#95a5a6', '#bdc3c7', '#ecf0f1']
        for i, txt in enumerate(text_levels):
            y1 = i * height_per
            y2 = (i+1) * height_per
            draw.rectangle([0, y1, OUTPUT_SIZE[0], y2], fill=colors[i % len(colors)])
            draw.text((OUTPUT_SIZE[0]//2, (y1+y2)//2), txt, fill='black', font=font_small, anchor='mm')
        return img

    @staticmethod
    def roll_safe(img, draw, top_text, bottom_text, font_small):
        """Roll Safe (tap forehead)"""
        img = Image.new('RGB', OUTPUT_SIZE, color='#2c3e50')
        draw = ImageDraw.Draw(img)
        draw.text((OUTPUT_SIZE[0]//2, OUTPUT_SIZE[1]//3), top_text, fill='white', font=font_small, anchor='mm')
        draw.text((OUTPUT_SIZE[0]//2, 2*OUTPUT_SIZE[1]//3), bottom_text, fill='#f1c40f', font=font_small, anchor='mm')
        return img

    @staticmethod
    def unexpected_john_cena(img, draw, text, font_large):
        """Unexpected meme (blank then pop)"""
        img = Image.new('RGB', OUTPUT_SIZE, color='#c0392b')
        draw = ImageDraw.Draw(img)
        draw.text((OUTPUT_SIZE[0]//2, OUTPUT_SIZE[1]//2), text, fill='white', font=font_large, anchor='mm')
        return img

    @staticmethod
    def indian_parents(img, draw, child_action, parent_reaction, font_small):
        """Indian parents template"""
        img = Image.new('RGB', OUTPUT_SIZE, color='#f4d03f')
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, OUTPUT_SIZE[0], OUTPUT_SIZE[1]//2], fill='#e67e22')
        draw.text((OUTPUT_SIZE[0]//2, OUTPUT_SIZE[1]//4), child_action, fill='white', font=font_small, anchor='mm')
        draw.text((OUTPUT_SIZE[0]//2, 3*OUTPUT_SIZE[1]//4), parent_reaction, fill='black', font=font_small, anchor='mm')
        return img

    @staticmethod
    def mr_incredible(img, draw, text1, text2, text3, text4, font_small):
        """Mr. Incredible becoming uncanny (4 stages)"""
        stages = [text1, text2, text3, text4]
        for i, txt in enumerate(stages):
            x = (i % 2) * OUTPUT_SIZE[0]//2
            y = (i // 2) * OUTPUT_SIZE[1]//2
            box = (x, y, x+OUTPUT_SIZE[0]//2, y+OUTPUT_SIZE[1]//2)
            draw.rectangle(box, fill=f'#{20+40*i:02x}{20+40*i:02x}{20+40*i:02x}')
            draw.text((x+OUTPUT_SIZE[0]//4, y+OUTPUT_SIZE[1]//4), txt, fill='white', font=font_small, anchor='mm')
        return img

# ------------------------------------------------------------
#  TREND FETCHER (real topics from Google Trends India)
# ------------------------------------------------------------
def get_indian_trends():
    """Fetch current trending topics in India with fallback"""
    trends = []
    try:
        url = "https://trends.google.com/trending/trendingsearches/daily?geo=IN"
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            # Quick and dirty parsing (avoids heavy libraries)
            import re
            titles = re.findall(r'"title":"([^"]+)"', resp.text)
            trends = titles[:20]
    except Exception as e:
        print(f"Trend fetch failed: {e}")
    if not trends:
        trends = random.sample(FALLBACK_TRENDS, min(15, len(FALLBACK_TRENDS)))
    return list(set(trends))  # remove duplicates

# ------------------------------------------------------------
#  CAPTION & HASHTAG GENERATOR (viral ready)
# ------------------------------------------------------------
def generate_viral_caption(trend, template_type):
    """Return a funny, relatable caption in Hinglish/English"""
    templates = {
        "drake": [f"Me: {trend} is serious\nAlso me: {trend} be like", f"{trend}? No thanks.\nBut memes about {trend}? Yes."],
        "two_buttons": [f"Button 1: Ignore {trend}\nButton 2: Make memes about {trend}", f"Normal life vs {trend} life"],
        "distracted_boyfriend": [f"Me ignoring {trend}\nLooking at {trend} memes", f"Girlfriend: {trend}\nMe: *thinking about {trend} memes*"],
        "change_my_mind": [f"{trend} is overrated. Change my mind.", f"Change my mind: {trend} is just an excuse to scroll reels."],
        "expanding_brain": [f"Understanding {trend}\nMaking memes on {trend}\nGoing viral with {trend}\nProfit??"],
        "roll_safe": [f"Can't handle {trend}? Just laugh at it.", f"{trend} solution: ignore and make memes"],
        "indian_parents": [f"Parents: Focus on studies\nMe: But {trend} is trending!", f"When {trend} happens and parents blame you"],
        "mr_incredible": [f"Normal {trend} → Relatable {trend} → Hilarious {trend} → Viral {trend} meme"]
    }
    captions = templates.get(template_type, [f"{trend} be like 😂 #relatable"])
    return random.choice(captions)

def generate_hashtags(trend):
    """Create 10 trending hashtags including Indian and generic viral ones"""
    base = trend.replace(" ", "").replace("-", "")
    return f"#{base} #{base}Memes #{base}Trending #IndianMemes #ViralHumor #Relatable #InstaReels #{base}KaChaska #MemeOfTheDay"

# ------------------------------------------------------------
#  TEXT EFFECTS (outline, shadow, gradient)
# ------------------------------------------------------------
def draw_text_with_outline(draw, xy, text, font, text_color, outline_color, stroke_width=2):
    x, y = xy
    # outline
    for dx in range(-stroke_width, stroke_width+1):
        for dy in range(-stroke_width, stroke_width+1):
            if dx != 0 or dy != 0:
                draw.text((x+dx, y+dy), text, fill=outline_color, font=font, anchor='mm')
    draw.text((x, y), text, fill=text_color, font=font, anchor='mm')

# ------------------------------------------------------------
#  MAIN MEME GENERATION ENGINE
# ------------------------------------------------------------
class MegaMemeBot:
    def __init__(self):
        self.templates = {
            "drake": MemeTemplates.drake,
            "two_buttons": MemeTemplates.two_buttons,
            "distracted_boyfriend": MemeTemplates.distracted_boyfriend,
            "change_my_mind": MemeTemplates.change_my_mind,
            "expanding_brain": MemeTemplates.expanding_brain,
            "roll_safe": MemeTemplates.roll_safe,
            "unexpected": MemeTemplates.unexpected_john_cena,
            "indian_parents": MemeTemplates.indian_parents,
            "mr_incredible": MemeTemplates.mr_incredible
        }
        self.font_large = None
        self.font_small = None
        self._load_fonts()
        self.generated_memes = []

    def _load_fonts(self):
        """Try to load custom fonts, fallback to default"""
        try:
            self.font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            self.font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        except:
            try:
                self.font_large = ImageFont.truetype("arialbd.ttf", 48)
                self.font_small = ImageFont.truetype("arial.ttf", 32)
            except:
                self.font_large = ImageFont.load_default()
                self.font_small = ImageFont.load_default()

    def generate_one_meme(self, trend, template_name, meme_id):
        """Create a single meme image and return metadata"""
        img = Image.new('RGB', OUTPUT_SIZE, color=random.choice(BACKGROUND_COLORS))
        draw = ImageDraw.Draw(img)
        
        # Generate dynamic text based on template
        if template_name == "drake":
            top = f"Taking {trend} seriously"
            bottom = f"Making memes about {trend}"
            img = self.templates[template_name](img, draw, top, bottom, self.font_large, self.font_small)
        elif template_name == "two_buttons":
            left = f"Scroll past {trend}"
            right = f"Make viral meme on {trend}"
            img = self.templates[template_name](img, draw, left, right, self.font_small)
        elif template_name == "distracted_boyfriend":
            girl = f"Other trends"
            guy = f"Me"
            new_girl = f"{trend} memes"
            img = self.templates[template_name](img, draw, girl, new_girl, guy, self.font_small)
        elif template_name == "change_my_ mind":
            text = f"{trend} is not that funny. Change my mind."
            img = self.templates[template_name](img, draw, text, self.font_large)
        elif template_name == "expanding_brain":
            levels = [
                f"{trend} happens",
                f"People discuss {trend}",
                f"Memes about {trend} appear",
                f"{trend} becomes legendary meme"
            ]
            img = self.templates[template_name](img, draw, levels, self.font_small)
        elif template_name == "roll_safe":
            top = f"Don't understand {trend}?"
            bottom = f"Just laugh at memes"
            img = self.templates[template_name](img, draw, top, bottom, self.font_small)
        elif template_name == "unexpected":
            img = self.templates[template_name](img, draw, f"{trend.upper()} BE LIKE...", self.font_large)
        elif template_name == "indian_parents":
            child = f"Me: {trend} is trending!"
            parent = f"Parents: Beta, padhai pe dhyan do!"
            img = self.templates[template_name](img, draw, child, parent, self.font_small)
        elif template_name == "mr_incredible":
            img = self.templates[template_name](img, draw, 
                f"Normal {trend}", f"Relatable {trend}", f"Hilarious {trend}", f"Viral {trend} meme",
                self.font_small)
        else:
            # Fallback: plain text on colored background
            draw.text((OUTPUT_SIZE[0]//2, OUTPUT_SIZE[1]//2), f"{trend} be like...", fill='white', font=self.font_large, anchor='mm')
        
        # Add watermark (account name)
        draw_text_with_outline(draw, (OUTPUT_SIZE[0]-80, OUTPUT_SIZE[1]-40), "@daily_indian_memes", self.font_small, 'white', 'black', stroke_width=2)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%d %b %Y")
        draw.text((50, OUTPUT_SIZE[1]-40), f"🔥 {timestamp}", fill='#dddddd', font=self.font_small)
        
        # Save image
        filename = f"viral_{template_name}_{trend.replace(' ', '_')}_{meme_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        img.save(filename)
        
        # Caption and hashtags
        caption = generate_viral_caption(trend, template_name)
        hashtags = generate_hashtags(trend)
        full_caption = f"{caption}\n\n{hashtags}"
        
        return {
            "image": filename,
            "caption": full_caption,
            "trend": trend,
            "template": template_name,
            "size": OUTPUT_SIZE
        }
    
    def generate_batch(self, count=NUMBER_OF_MEMES):
        """Generate a batch of memes using random trends and templates"""
        trends = get_indian_trends()
        if not trends:
            trends = FALLBACK_TRENDS
        available_templates = list(self.templates.keys())
        
        memes = []
        for i in range(count):
            trend = random.choice(trends)
            template = random.choice(available_templates)
            print(f"Creating meme {i+1}/{count}: {trend} using {template}")
            meme_data = self.generate_one_meme(trend, template, i+1)
            memes.append(meme_data)
            time.sleep(0.3)  # be gentle on resources
        
        # Save metadata
        with open("meme_batch_metadata.json", "w", encoding='utf-8') as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "total_memes": len(memes),
                "memes": memes
            }, f, indent=2, ensure_ascii=False)
        
        self.generated_memes = memes
        return memes

# ------------------------------------------------------------
#  SOCIAL MEDIA POSTING (stubs – replace with real APIs)
# ------------------------------------------------------------
def post_to_instagram(meme_info):
    """Post to Instagram Business Account"""
    # Real implementation would use Facebook Graph API
    print(f"📸 INSTAGRAM: {meme_info['image']} with caption {meme_info['caption'][:50]}...")
    return True

def post_to_facebook(meme_info, page_id=None):
    """Post to Facebook Page"""
    print(f"📘 FACEBOOK: {meme_info['image']} with caption {meme_info['caption'][:50]}...")
    return True

def post_to_twitter(meme_info):
    """Post to Twitter/X"""
    print(f"🐦 TWITTER: {meme_info['image']} posted")
    return True

def post_all(memes):
    """Post all memes to every connected platform"""
    for meme in memes:
        post_to_instagram(meme)
        post_to_facebook(meme)
        post_to_twitter(meme)
    print("✅ All memes posted!")

# ------------------------------------------------------------
#  MAIN EXECUTION (runs when script is called)
# ------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Mega Meme Bot starting...")
    bot = MegaMemeBot()
    memes = bot.generate_batch(NUMBER_OF_MEMES)
    print(f"✅ Generated {len(memes)} memes.")
    
    # If you have environment variables with access tokens, uncomment:
    # if os.environ.get("POST_TO_SOCIAL") == "true":
    #     post_all(memes)
    
    # Save list of images for GitHub Actions artifact
    with open("generated_files.txt", "w") as f:
        for m in memes:
            f.write(m["image"] + "\n")
    print("🎉 Done!")
