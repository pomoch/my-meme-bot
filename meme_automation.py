import random
import json
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Simplified meme generator for kids
class SimpleMemeBot:
    def __init__(self):
        self.topics = ["IPL Cricket", "Bollywood Drama", "School Exams", "Monsoon Rains", "Mobile Games"]
        
    def make_meme(self, topic, number):
        # Create a simple image
        img = Image.new('RGB', (800, 600), color='white')
        draw = ImageDraw.Draw(img)
        # Use default font (no need to download)
        font = ImageFont.load_default()
        
        # Write the meme text
        draw.text((50, 50), f"MEME #{number}", fill='black', font=font)
        draw.text((50, 100), f"Topic: {topic}", fill='black', font=font)
        draw.text((50, 200), f"When you see {topic} trending:", fill='black', font=font)
        draw.text((50, 300), "😂🤣😂", fill='black', font=font)
        
        # Save the image
        filename = f"meme_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{number}.png"
        img.save(filename)
        return filename
    
    def generate_memes(self, count=5):
        memes = []
        for i in range(count):
            topic = random.choice(self.topics)
            image_file = self.make_meme(topic, i+1)
            caption = f"🤣 {topic} be like! #meme #funny #india"
            memes.append({"image": image_file, "caption": caption})
        
        # Save the list to a file
        with open("daily_memes.json", "w") as f:
            json.dump(memes, f)
        return memes

if __name__ == "__main__":
    bot = SimpleMemeBot()
    bot.generate_memes()
    print("✅ Memes created!")
