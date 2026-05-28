import requests
import random

def generate_fashion_images(prompt):
    """Free unlimited image generation via Pollinations.ai"""
    encoded_prompt = requests.utils.quote(prompt)
    seed = random.randint(1, 100000)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"
    return url
