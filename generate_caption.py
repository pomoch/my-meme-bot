import requests
import random

# Hand-crafted fallback captions (modern, flirty, emoji-rich)
FALLBACK_CAPTIONS = [
    "Living my best life, one outfit at a time ✨",
    "New day, new slay 💁‍♀️",
    "Just because it's Tuesday doesn't mean I can't sparkle 💖",
    "Confidence level: selfie with no filter 📸",
    "Catch me in the front row of my own life 🎬",
    "Serving looks, not tea ☕️",
    "Making ordinary moments extraordinary 💫",
    "Too glam to give a damn 💅",
    "Not everyone’s cup of tea, but I’m someone’s shot of tequila 🥃",
    "Sunshine mixed with a little hurricane 🌪️",
    "Be your own kind of beautiful 🌸",
    "Smiling because I know something you don’t 😏",
    "Life’s a party, dress like it 🎉",
    "I’m not perfect, but my outfit is 👗",
    "Chapter one of a thousand adventures 📖",
    "Powered by caffeine and ambition ☕️",
    "Dream big, sparkle more, shine bright ✨",
    "Doing it for the plot 📚",
    "Messy bun and getting stuff done 💪",
    "Sunkissed and blessed ☀️",
    "Chasing sunsets and dreams 🌅",
    "On my worst behavior 😈",
    "Good vibes only (and a little mischief) 😜",
    "Proof that I do leave the house sometimes 🏠",
    "If you were looking for a sign, here it is 💫",
    "Just a girl with big goals and a bigger closet 🛍️",
    "Keep your heels, head, and standards high 👠",
    "Darling, you’re a work of art 🖼️",
    "Don’t study me, you won’t graduate 🎓",
    "Life isn’t perfect, but my outfit is 👌",
    "Making the world my runway 🏃‍♀️",
    "I’m the girl you’ve been warned about 🔥",
    "Sugar, spice, and everything nice (mostly spice) 🌶️",
    "No rain, no flowers 🌧️🌸",
    "You can’t do epic shit with basic people 💅"
]

def create_caption(context):
    # Try the free text API
    prompt = (
        f"Write a short, engaging Instagram caption for an AI influencer. "
        f"Context: {context}. Keep under 200 characters. Use emojis. Sound natural and flirty."
    )
    encoded = requests.utils.quote(prompt)
    url = f"https://text.pollinations.ai/{encoded}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200 and resp.text.strip():
            return resp.text.strip()
    except:
        pass
    # Fallback
    return random.choice(FALLBACK_CAPTIONS)
