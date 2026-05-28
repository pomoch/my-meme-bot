from moviepy import (
    ImageClip, CompositeVideoClip, concatenate_videoclips,
    TextClip, ColorClip, vfx
)
import numpy as np
import random
import cv2
import os

def ken_burns_effect(clip, duration=3.0, zoom_ratio=0.04, pan_range=0.05):
    w, h = clip.size
    x_shift = int(w * pan_range * (random.random() - 0.5))
    y_shift = int(h * pan_range * (random.random() - 0.5))
    
    def make_frame(t):
        progress = t / duration if duration > 0 else 0
        zoom = 1 + zoom_ratio * progress
        new_w = int(w * zoom)
        new_h = int(h * zoom)
        center_x = (new_w - w) / 2 + x_shift * progress
        center_y = (new_h - h) / 2 + y_shift * progress
        resized = clip.resized((new_w, new_h))
        return resized.cropped(x1=center_x, y1=center_y, width=w, height=h).get_frame(t)
    
    return clip.transform(make_frame, duration=duration)

def add_wiggle(clip):
    def wiggle_frame(t):
        frame = clip.get_frame(t)
        shift = int(10 * np.sin(2 * np.pi * 3 * t))
        M = np.float32([[1, 0, shift], [0, 1, 0]])
        return cv2.warpAffine(frame, M, (clip.w, clip.h))
    return clip.transform(wiggle_frame)

def sharpen_frame(clip):
    """Sharpen every frame with a strong kernel."""
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]], dtype=np.float32)
    def make_sharp(t):
        frame = clip.get_frame(t)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        sharpened_bgr = cv2.filter2D(frame_bgr, -1, kernel)
        sharpened_rgb = cv2.cvtColor(sharpened_bgr, cv2.COLOR_BGR2RGB)
        return sharpened_rgb
    return clip.transform(make_sharp)

def create_themed_video(image_paths, title_text="✨ Video ✨",
                        video_style="slow", wiggle=False,
                        output="daily_video.mp4"):
    # Check image existence
    for img in image_paths:
        if not os.path.exists(img):
            raise FileNotFoundError(f"Image {img} not found")
    
    if video_style == "fast":
        duration = 1.5
        zoom_ratio = 0.02
    elif video_style == "medium":
        duration = 2.0
        zoom_ratio = 0.03
    else:
        duration = 2.5
        zoom_ratio = 0.04

    clips = []
    # Title clip – try common fonts, fallback to default
    try:
        txt = TextClip(
            text=title_text,
            font_size=70,
            color='white',
            font='Arial-Bold',
            stroke_color='black',
            stroke_width=3,
            size=(1080, 200)
        )
    except:
        # Fallback to default font if Arial not available
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
    title_clip = CompositeVideoClip([bg, txt], size=(1080, 1350))
    clips.append(title_clip)

    for img_path in image_paths:
        clip = ImageClip(img_path).resized((1080, 1350))
        clip = ken_burns_effect(clip, duration=duration, zoom_ratio=zoom_ratio, pan_range=0.03)
        clip = sharpen_frame(clip)
        if wiggle:
            clip = add_wiggle(clip)
        clips.append(clip)

    padding = -0.8 if video_style == "fast" else -1.0
    final = concatenate_videoclips(clips, method="compose", padding=padding)
    final = final.with_effects([vfx.FadeIn(0.5), vfx.FadeOut(0.5)])

    # Use libx264rgb for better color quality
    final.write_videofile(output, fps=24, codec="libx264rgb", audio=False, preset="medium", bitrate="8000k")
    
    if not os.path.exists(output):
        raise RuntimeError("Video rendering failed – output file not created")
    return output
