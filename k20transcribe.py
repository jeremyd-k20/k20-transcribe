import streamlit as st
from google import genai
from google.genai import types
import time

client = genai.Client()

st.title("YouTube Career Interview Transcriber")
url = st.text_input("Enter YouTube Video URL:")

def generate_transcript_from_youtube(video_url):
    # Construct a FileData part specifically for YouTube URLs
    video_part = types.Part(
        file_data=types.FileData(file_uri=video_url)
    )
    
    prompt = [
        video_part,
        "Please transcribe this video accurately. Format the transcript with clear speaker labels (e.g., Interviewer, Guest) and natural paragraph breaks."
    ]
    
    # Try primary model first, fallback to flash-lite if busy
    models_to_try = ['gemini-3.8-flash', 'gemini-3.5-flash-lite']
    
    for model_name in models_to_try:
        for attempt in range(1, 3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return response
            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    time.sleep(2)
                    continue
                else:
                    raise e

    raise Exception("All API models are currently experiencing high traffic. Please try again in 1 minute.")

if st.button("Generate Transcript") and url:
    try:
        with st.spinner("Gemini is fetching and analyzing the video..."):
            response = generate_transcript_from_youtube(url)

        st.subheader("Transcript")
        st.write(response.text)

    except Exception as e:
        st.error(f"Error: {str(e)}")
