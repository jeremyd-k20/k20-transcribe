import streamlit as st
from google import genai
import time

client = genai.Client()

st.title("YouTube Career Interview Transcriber")
url = st.text_input("Enter YouTube Video URL:")

def generate_transcript_with_retry(video_url, max_retries=3):
    """Retries up to max_retries if the Gemini API is busy or overloaded."""
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=[
                    f"Please transcribe this YouTube video accurately: {video_url}",
                    "Format the transcript with clear speaker labels (e.g., Interviewer, Guest) and natural paragraph breaks."
                ]
            )
            return response
        except Exception as e:
            # If we run out of retries, raise the exception to display to the user
            if attempt == max_retries:
                raise e
            # Wait 3 seconds before retrying
            time.sleep(3)

if st.button("Generate Transcript") and url:
    try:
        with st.spinner("Gemini is analyzing the video (this may take up to a minute)..."):
            response = generate_transcript_with_retry(url)

        st.subheader("Transcript")
        st.write(response.text)

    except Exception as e:
        st.error(f"The model is currently experiencing high traffic. Please wait 10 seconds and try again. (Error detail: {str(e)})")
