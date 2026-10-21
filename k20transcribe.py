import streamlit as st
from google import genai
from google.genai import types
import time

client = genai.Client()

st.title("YouTube Career Interview Transcriber")
url = st.text_input("Enter YouTube Video URL:")

def generate_formatted_transcript(video_url):
    video_part = types.Part(
        file_data=types.FileData(file_uri=video_url)
    )
    
    # Detailed prompt instructions for clean readability
    system_instructions = (
        "You are an expert transcription assistant. Please transcribe the provided video with the following strict formatting rules:\n"
        "1. Identify the main speakers (e.g., 'Interviewer', 'Guest', or by actual name if introduced) and start each speaker's block with their name in bold (e.g., **Interviewer:**, **Kristen:**).\n"
        "2. Place a clear double line break (blank line) every time the speaker changes.\n"
        "3. Break long mono-speaker answers into smaller, natural paragraphs for easy reading.\n"
        "4. Remove unnecessary non-verbal noise markers like [Music], [Applause], or [Laughter] unless critical to context.\n"
        "5. Output clean Markdown text."
    )
    
    prompt = [video_part, system_instructions]
    
    # Models to try in order of efficiency
    models_to_try = ['gemini-3.5-flash-lite', 'gemini-3.8-flash']
    
    for model_name in models_to_try:
        for attempt in range(1, 3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return response
            except Exception as e:
                if "503" in str(e) or "429" in str(e) or "UNAVAILABLE" in str(e):
                    time.sleep(3)
                    continue
                else:
                    raise e

    raise Exception("API quotas are currently limit-reached or models are busy. Please try again later.")

if st.button("Generate Transcript") and url:
    try:
        with st.spinner("Gemini is transcribing and formatting the video..."):
            response = generate_formatted_transcript(url)

        st.subheader("Formatted Transcript")
        st.markdown(response.text)

    except Exception as e:
        st.error(f"Error: {str(e)}")
