import streamlit as st
from google import genai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.genai.errors import APIError

client = genai.Client()

st.title("YouTube Career Interview Transcriber")
url = st.text_input("Enter YouTube Video URL:")

# Retry helper: Retries up to 3 times if a 503 or API error occurs
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry_error_cls=APIError
)
def generate_transcript_with_retry(video_url):
    return client.models.generate_content(
        model='gemini-3.8-flash',
        contents=[
            f"Please transcribe this YouTube video accurately: {video_url}",
            "Format the transcript with clear speaker labels (e.g., Interviewer, Guest) and natural paragraph breaks."
        ]
    )

if st.button("Generate Transcript") and url:
    try:
        with st.spinner("Gemini is analyzing the video..."):
            response = generate_transcript_with_retry(url)

        st.subheader("Transcript")
        st.write(response.text)

    except Exception as e:
        st.error(f"The model is currently busy. Please wait a moment and try again. (Details: {str(e)})")
