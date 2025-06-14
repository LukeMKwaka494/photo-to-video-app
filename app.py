import streamlit as st
from moviepy.editor import ImageSequenceClip, AudioFileClip
import os
import tempfile

st.title("📸 Photo to Video with Audio")

uploaded_images = st.file_uploader("Upload Images (PNG/JPG)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
uploaded_audio = st.file_uploader("Upload Background Music (MP3/WAV)", type=["mp3", "wav"])
fps = st.slider("Select video speed (FPS)", 1, 30, 5)

if uploaded_images and uploaded_audio:
    with tempfile.TemporaryDirectory() as tmpdir:
        image_paths = []
        for i, img in enumerate(uploaded_images):
            path = os.path.join(tmpdir, f"{i}.png")
            with open(path, "wb") as f:
                f.write(img.getbuffer())
            image_paths.append(path)

        audio_path = os.path.join(tmpdir, "audio.mp3")
        with open(audio_path, "wb") as f:
            f.write(uploaded_audio.getbuffer())

        st.info("Generating video...")
        clip = ImageSequenceClip(image_paths, fps=fps)
        audioclip = AudioFileClip(audio_path)
        clip = clip.set_audio(audioclip)
        output_path = os.path.join(tmpdir, "final_video.mp4")
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        with open(output_path, "rb") as f:
            st.download_button("Download Your Video 🎬", f, "video_with_audio.mp4", "video/mp4")
