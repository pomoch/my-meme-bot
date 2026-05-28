import requests, random

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
    "You can’t do epic shit with basic people 💅",
    "In a world full of trends, I choose to be a classic 🎞️",
    "Own who you are 💎",
    "Cinderella never asked for a prince – she asked for a night off ✨",
    "I’m not shy, I’m just observing my future subjects 👑",
    "Be a voice, not an echo 🗣️",
    "I woke up like this (after 3 cups of coffee) ☕️",
    "Reality called, so I hung up 📞",
    "I’m on a seafood diet – I see food and I eat it 🍕",
    "When nothing goes right, go left ↩️",
    "A beautiful day to be a badass 😎",
    "I don’t sweat – I sparkle ✨",
    "Life is short, make every outfit count 👗",
    "Be the energy you want to attract 🔮",
    "Born to stand out, not fit in 🌈",
    "Sparkle like you mean it 💖",
    "Dress like you’re already famous 📸",
    "Be a flamingo in a flock of pigeons 🦩",
    "My vibe speaks louder than words 🔊",
    "Chin up, buttercup 🌼",
    "Today’s goal: be the reason someone smiles 😊"
]

def create_caption(context):
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
    return random.choice(FALLBACK_CAPTIONS)
