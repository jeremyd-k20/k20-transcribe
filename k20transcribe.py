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
    
    # Custom formatting instructions provided by your team
    system_instructions = (
        "You are an expert transcription assistant. Please transcribe the provided video adhering strictly to the following formatting guidelines:\n\n"
        "1. **Speaker Names:**\n"
        "   - Use the speaker's **Full Name** (First and Last name) the very first time they speak.\n"
        "   - For all subsequent turns, use only their **First Name** (or how they are primarily referenced in the video).\n"
        "   - Always **bold** the name of the speaker (e.g., **Fabiola McComb:**, **Kristen Garcia:**, **Kristen:**).\n\n"
        "2. **Dialogue & Paragraphs:**\n"
        "   - Put a clear double line break (blank line) every time the speaker changes.\n"
        "   - Break long answers into smaller, readable paragraphs.\n"
        "   - Use standard quotation marks `\" \"` when a speaker is quoting someone (e.g., Dolly said \"x\").\n\n"
        "3. **Audio Cues & Noise:**\n"
        "   - Use parentheses and italics for vocalized non-speech sounds or actions, e.g., (*laughter*), (*applause*).\n"
        "   - Omit repetitive background musical markers like `[Music]` unless essential to context.\n\n"
        "4. **Clean Readability:**\n"
        "   - Remove filler words (such as 'um', 'uh', 'like', 'you know', 'etc.') to produce a polished, professional transcript.\n"
        "   - Output cleanly rendered Markdown text."
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
