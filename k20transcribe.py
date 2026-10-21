import streamlit as st
from google import genai
from google.genai import types
import time

client = genai.Client()

st.title("YouTube Career Interview Transcriber")
url = st.text_input("Enter YouTube Video URL:")

def generate_transcript_from_youtube(video_url):
    video_part = types.Part(
        file_data=types.FileData(file_uri=video_url)
    )
    
    prompt = [
        video_part,
        "Please transcribe this video accurately. Format the transcript with clear speaker labels (e.g., Interviewer, Guest) and natural paragraph breaks."
    ]
    
    # Prioritizes flash-lite for higher throughput
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
                # If experiencing rate limits or traffic spikes, wait briefly and retry/switch
                if "503" in str(e) or "429" in str(e) or "UNAVAILABLE" in str(e):
                    time.sleep(3)
                    continue
                else:
                    raise e

    raise Exception("API quotas are currently limit-reached or models are busy. Please try again later.")

if st.button("Generate Transcript") and url:
    try:
        with st.spinner("Gemini Flash-Lite is processing the video..."):
            response = generate_transcript_from_youtube(url)

        st.subheader("Transcript")
        st.write(response.text)

    except Exception as e:
        st.error(f"Error: {str(e)}")
