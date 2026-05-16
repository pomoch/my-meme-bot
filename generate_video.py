from moviepy import ImageClip, concatenate_videoclips

def create_transition_video(image_paths, output="output.mp4", duration_per_image=2):
    """
    Stitch images into a short video with fade transitions.
    Works with MoviePy v2.x.
    """
    clips = []
    for img in image_paths:
        # Create a still image clip with the given duration
        clip = ImageClip(img, duration=duration_per_image)
        clips.append(clip)

    # Concatenate all clips with a crossfade (1 second fade) between them
    # concatenate_videoclips with transition supports a fade effect
    final = concatenate_videoclips(clips, method="compose", padding=-1)
    # Add fadein at start and fadeout at end for smoothness
    final = final.with_effects([("fadein", 0.5), ("fadeout", 0.5)])

    final.write_videofile(output, fps=24, codec="libx264", audio=False)
    return output
