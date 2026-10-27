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
    
    # PASS 1: Transcribe audio and structure speaker turns
    pass1_instructions = (
        "You are an expert transcription assistant. Transcribe the provided video with the following formatting:\n\n"
        "1. Speaker Names: Use the speaker's Full Name (First and Last name) the very first time they speak. "
        "For all subsequent turns, use only their First Name. Always bold the speaker's name (e.g., **Fabiola McComb:**, **Kristen Garcia:**, **Kristen:**).\n"
        "2. Dialogue & Paragraphs: Put a clear double line break (blank line) every time the speaker changes. "
        "Break long answers into smaller, readable paragraphs. Use standard quotation marks \" \" when a speaker is quoting someone.\n"
        "3. Audio Cues: Use parentheses and italics for vocalized non-speech sounds or actions, e.g., (*laughter*), (*applause*). "
        "Omit repetitive background musical markers like [Music].\n"
        "4. Capture all spoken dialogue accurately."
    )
    
    prompt_pass1 = [video_part, pass1_instructions]
    
    models_to_try = ['gemini-3.5-flash-lite', 'gemini-3.8-flash']
    raw_transcript = None
    
    # Execute Pass 1: Audio Transcription
    for model_name in models_to_try:
        for attempt in range(1, 3):
            try:
                response1 = client.models.generate_content(
                    model=model_name,
                    contents=prompt_pass1
                )
                raw_transcript = response1.text
                break
            except Exception as e:
                if "503" in str(e) or "429" in str(e) or "UNAVAILABLE" in str(e):
                    time.sleep(3)
                    continue
                else:
                    raise e
        if raw_transcript:
            break

    if not raw_transcript:
        raise Exception("Unable to process audio. Please try again later.")

    # PASS 2: Copy Editing & Strict Filler Word Removal
    pass2_instructions = (
        "You are a meticulous copy editor. Below is a transcript of an interview. "
        "Your sole task is to clean up speech disfluencies while preserving the exact layout, speaker labels, bolding, and meaning.\n\n"
        "STRICT EDITING RULES:\n"
        "1. Completely remove ALL filler words and verbal pauses: 'um', 'uh', 'like', 'you know', 'so', 'well', 'I mean', 'kind of', 'sort of'.\n"
        "2. Fix stutters and repeated false starts (e.g., change 'I I think' to 'I think', 'I'm I'm going' to 'I'm going').\n"
        "3. Keep all bold speaker tags (**Name:**) and structural line breaks exactly as they appear.\n"
        "4. Keep italicized sound effects like (*laughter*) intact.\n"
        "5. Output ONLY the finalized clean Markdown transcript.\n\n"
        f"TRANSCRIPT TO EDIT:\n{raw_transcript}"
    )

    # Execute Pass 2: Text Cleanup
    for model_name in models_to_try:
        for attempt in range(1, 3):
            try:
                response2 = client.models.generate_content(
                    model=model_name,
                    contents=pass2_instructions
                )
                return response2.text
            except Exception as e:
                if "503" in str(e) or "429" in str(e) or "UNAVAILABLE" in str(e):
                    time.sleep(2)
                    continue
                else:
                    raise e

    raise Exception("API models are busy. Please try again in 1 minute.")

if st.button("Generate Transcript") and url:
    try:
        with st.spinner("Step 1/2: Transcribing video audio..."):
            # Progress status update
            time.sleep(0.5)
            
        with st.spinner("Step 2/2: Removing filler words and formatting transcript..."):
            final_transcript = generate_formatted_transcript(url)

        st.subheader("Formatted Transcript")
        st.markdown(final_transcript)

    except Exception as e:
        st.error(f"Error: {str(e)}")
