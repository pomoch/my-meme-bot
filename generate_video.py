import os
import traceback
import numpy as np
import cv2
from moviepy import (
    ImageClip, CompositeVideoClip, concatenate_videoclips,
    TextClip, ColorClip, vfx
)
import random

def ken_burns(clip, duration, zoom_ratio=0.04):
    w, h = clip.size
    x_shift = int(w * 0.03 * (random.random() - 0.5))
    y_shift = int(h * 0.03 * (random.random() - 0.5))
    def make_frame(t):
        progress = t / duration if duration > 0 else 0
        zoom = 1 + zoom_ratio * progress
        new_w, new_h = int(w*zoom), int(h*zoom)
        cx = (new_w - w)/2 + x_shift*progress
        cy = (new_h - h)/2 + y_shift*progress
        return clip.resized((new_w, new_h)).cropped(x1=cx, y1=cy, width=w, height=h).get_frame(t)
    return clip.transform(make_frame, duration=duration)

def wiggle_effect(clip):
    def wiggle(t):
        frame = clip.get_frame(t)
        shift = int(8 * np.sin(2*np.pi*4*t))
        M = np.float32([[1,0,shift],[0,1,0]])
        return cv2.warpAffine(frame, M, (clip.w, clip.h))
    return clip.transform(wiggle)

def sharpen_clip(clip):
    kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]], dtype=np.float32)
    def sharp(t):
        frame = clip.get_frame(t)
        bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        sharp_bgr = cv2.filter2D(bgr, -1, kernel)
        return cv2.cvtColor(sharp_bgr, cv2.COLOR_BGR2RGB)
    return clip.transform(sharp)

def create_themed_video(image_paths, title_text, video_style="slow", wiggle=False, output="daily_video.mp4"):
    try:
        # Verify images exist
        for p in image_paths:
            if not os.path.exists(p):
                raise FileNotFoundError(f"Missing image: {p}")

        # Style settings
        if video_style == "fast":
            dur = 1.5
            zoom = 0.02
        elif video_style == "medium":
            dur = 2.0
            zoom = 0.03
        else:
            dur = 2.5
            zoom = 0.04

        clips = []

        # Title clip – use a simple approach without external fonts
        try:
            # Try to use default font
            txt = TextClip(
                text=title_text,
                font_size=70,
                color='white',
                stroke_color='black',
                stroke_width=3,
                size=(1080, 200),
                font='Arial-Bold'  # safe fallback
            )
        except:
            txt = TextClip(
                text=title_text,
                font_size=70,
                color='white',
                stroke_color='black',
                stroke_width=3,
                size=(1080, 200)
            )
        txt = txt.with_position(('center', 'center')).with_duration(1.5)
        bg = ColorClip(size=(1080, 1350), color=(0,0,0)).with_duration(1.5)
        title = CompositeVideoClip([bg, txt], size=(1080, 1350))
        clips.append(title)

        # Process images
        for path in image_paths:
            clip = ImageClip(path).resized((1080, 1350))
            clip = ken_burns(clip, dur, zoom)
            clip = sharpen_clip(clip)
            if wiggle:
                clip = wiggle_effect(clip)
            clips.append(clip)

        # Concatenate with crossfade
        padding = -0.8 if video_style == "fast" else -1.0
        final = concatenate_videoclips(clips, method="compose", padding=padding)
        final = final.with_effects([vfx.FadeIn(0.5), vfx.FadeOut(0.5)])

        # Write with robust settings
        final.write_videofile(
            output,
            fps=24,
            codec="libx264",
            audio=False,
            preset="fast",
            bitrate="5000k",
            verbose=False,
            logger=None
        )
        print("✅ MoviePy rendering finished.")
    except Exception as e:
        print(f"❌ MoviePy error: {e}")
        traceback.print_exc()
        # Do not re-raise; let main.py handle fallback
