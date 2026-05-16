import requests
import random

def generate_fashion_images(prompt):
    """Use Pollinations.ai – free, no key required."""
    # Pollinations URL format: https://image.pollinations.ai/prompt/{prompt}?seed={seed}&width=1024&height=1024&nologo=true
    encoded_prompt = requests.utils.quote(prompt)
    # Add a random seed for variety
    seed = random.randint(1, 100000)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"
    
    # Pollinations returns the image directly as the response content
    # But we only need the URL for now, our main.py downloads it
    return url
