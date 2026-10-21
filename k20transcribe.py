import streamlit as st
from google import genai
import time

client = genai.Client()

st.title("YouTube Career Interview Transcriber")
url = st.text_input("Enter YouTube Video URL:")

def generate_transcript_with_fallback(video_url):
    """Tries the primary model with retries, then falls back to Flash Lite if busy."""
    prompt = [
        f"Please transcribe this YouTube video accurately: {video_url}",
        "Format the transcript with clear speaker labels (e.g., Interviewer, Guest) and natural paragraph breaks."
    ]
    
    # List of models to try in order
    models_to_try = ['gemini-3.8-flash', 'gemini-3.5-flash-lite']
    
    for model_name in models_to_try:
        for attempt in range(1, 3):  # 2 attempts per model
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return response
            except Exception as e:
                # If 503/busy error occurs, wait briefly before retrying or switching models
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    time.sleep(2)
                    continue
                else:
                    # If it's a non-503 error, raise immediately
                    raise e

    # If all retries on all models fail:
    raise Exception("All API models are currently experiencing high traffic. Please try again in 1 minute.")

if st.button("Generate Transcript") and url:
    try:
        with st.spinner("Gemini is processing the video..."):
            response = generate_transcript_with_fallback(url)

        st.subheader("Transcript")
        st.write(response.text)

    except Exception as e:
        st.error(f"Error: {str(e)}")
