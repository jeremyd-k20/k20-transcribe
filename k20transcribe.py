import streamlit as st
from google import genai
import yt_dlp
import os

# Initialize Gemini Client (requires GEMINI_API_KEY environment variable)
client = genai.Client()

st.title("YouTube Career Interview Transcriber")
url = st.text_input("Enter YouTube Video URL:")

if st.button("Generate Transcript") and url:
    with st.spinner("Fetching audio from YouTube..."):
        # Configure yt-dlp to download lightweight audio
        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'outtmpl': 'temp_audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    with st.spinner("Processing audio with Gemini..."):
        # Upload the extracted audio to Gemini Files API
        audio_file = client.files.upload(file="temp_audio.m4a")
        
        # Prompt Gemini to transcribe and format
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                audio_file,
                "Transcribe this interview accurately. Identify speakers (e.g., Interviewer, Guest) where clear, and format with paragraph breaks for readability."
            ]
        )
        
        # Cleanup local file
        os.remove("temp_audio.m4a")

    st.subheader("Transcript")
    st.write(response.text)