import streamlit as st
from google import genai

# Initialize Gemini Client (uses GEMINI_API_KEY from Streamlit Secrets)
client = genai.Client()

st.title("YouTube Career Interview Transcriber")
url = st.text_input("Enter YouTube Video URL:")

if st.button("Generate Transcript") and url:
    try:
        with st.spinner("Gemini is analyzing the video..."):
            # Pass the YouTube link directly to the gemini-3.8-flash model
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=[
                    f"Please transcribe this YouTube video accurately: {url}",
                    "Format the transcript with clear speaker labels (e.g., Interviewer, Guest) and natural paragraph breaks."
                ]
            )

        st.subheader("Transcript")
        st.write(response.text)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
