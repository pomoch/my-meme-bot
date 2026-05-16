from moviepy import ImageClip, concatenate_videoclips
from moviepy.video.fx import FadeIn, FadeOut

def create_transition_video(image_paths, output="output.mp4", duration_per_image=2):
    """
    Stitch images into a short video with fade-in/out effects.
    Works with MoviePy v2.2.1+.
    """
    clips = []
    for img in image_paths:
        clip = ImageClip(img, duration=duration_per_image)
        clips.append(clip)

    # Concatenate without crossfade (just sequential)
    final = concatenate_videoclips(clips, method="chain")

    # Apply fade-in at start and fade-out at end
    final = final.with_effects([FadeIn(0.5), FadeOut(0.5)])

    final.write_videofile(output, fps=24, codec="libx264", audio=False)
    return output
