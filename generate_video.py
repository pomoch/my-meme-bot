from moviepy.editor import ImageSequenceClip, concatenate_videoclips
import os

def create_transition_video(image_paths, output="output.mp4", duration_per_image=2):
    """Stitches images into a short video with crossfade transition."""
    clips = []
    for img in image_paths:
        clip = ImageSequenceClip([img], durations=[duration_per_image])
        clips.append(clip)
    
    final = concatenate_videoclips(clips, method="compose")
    # Add a crossfade effect (simple fadein/out)
    final = final.crossfadein(0.5).crossfadeout(0.5)
    final.write_videofile(output, fps=24, codec="libx264", audio=False)
    return output
