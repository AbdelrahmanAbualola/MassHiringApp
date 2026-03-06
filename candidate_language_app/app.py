import streamlit as st
import os
import io
import re
from services.speech_analysis import transcribe_audio
from services.email_service import send_application_email, DEFAULT_RECIPIENT
from utils.audio_processing import process_audio, get_audio_duration
from utils.scoring import calculate_proficiency_score, get_cefr_level
from streamlit_mic_recorder import mic_recorder

# Application Configuration
st.set_page_config(page_title="Candidate Language Proficiency App", layout="centered")

def validate_phone(phone_number):
    """
    Validates the format of the phone number using a simple regex.
    """
    pattern = r'^\+?[\d\s-]{10,20}$'
    return re.match(pattern, phone_number) is not None

def main():
    st.title("Candidate Language Application")
    st.markdown("Please complete the following form to apply.")

    # 1. Candidate Information
    with st.form("candidate_application_form"):
        st.subheader("Candidate Information")
        name = st.text_input("Full Name", placeholder="Enter your full name", key="name")
        phone = st.text_input("Phone Number", placeholder="Enter your phone number (e.g., +1234567890)", key="phone")

        # 2. Resume Upload
        resume = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"], key="resume")

        # 3. Desired Language
        language = st.selectbox("Desired Language for Proficiency Test", ["English", "German", "Italian"], key="language")

        # Note: We can't put the mic_recorder or file_uploader (for audio) directly inside
        # a st.form if we want them to interact with the UI immediately or use
        # custom logic. However, the requirements ask for a form.
        # For simplicity, we'll collect all information and use a single "Submit"
        # button, but some components may need to be outside the literal st.form.

        # Since streamlit-mic-recorder doesn't work well inside st.form,
        # we will handle the submission logic outside or use a regular button.
        submit_button = st.form_submit_button("Submit Application")

    # 4. Voice Recording & Audio File Upload (Outside the form for better interaction)
    st.subheader("Voice Recording")
    st.info("Record a short message in your selected language (at least 5-10 seconds).")

    audio_data = None
    audio_type = None

    # Option A: Record Audio
    st.write("Option A: Record directly in the browser")
    recording = mic_recorder(
        start_prompt="Start Recording",
        stop_prompt="Stop Recording",
        just_once=False,
        use_recorder=True,
        key="recorder"
    )

    if recording:
        audio_data = recording['bytes']
        audio_type = 'wav' # streamlit-mic-recorder returns WAV bytes
        st.audio(audio_data, format='audio/wav')

    # Option B: Upload Audio File
    st.write("Option B: Upload an audio file (WAV, MP3, M4A)")
    audio_file_upload = st.file_uploader("Select an audio file", type=["wav", "mp3", "m4a"], key="audio_upload")

    if audio_file_upload:
        audio_data = audio_file_upload.read()
        audio_type = audio_file_upload.name.split('.')[-1]
        st.audio(audio_data, format=f'audio/{audio_type}')

    # 5. Handling Submission
    if submit_button:
        # Validation
        if not name:
            st.error("Candidate Name is required.")
            return
        if not phone:
            st.error("Candidate Phone Number is required.")
            return
        if not validate_phone(phone):
            st.error("Invalid phone number format. Please enter a valid number (e.g., +1234567890).")
            return
        if not resume:
            st.error("Please upload your resume.")
            return
        if not audio_data:
            st.error("Please provide a voice recording (either record or upload).")
            return

        with st.spinner("Processing your application and analyzing speech proficiency..."):
            try:
                # 5.1 Speech Processing
                # Convert to unique temporary WAV for processing
                temp_audio_path = process_audio(audio_data, audio_type)

                # Transcribe
                analysis = transcribe_audio(temp_audio_path, language=language)

                # Scoring
                duration = get_audio_duration(temp_audio_path)
                score = calculate_proficiency_score(analysis['confidence'], duration)
                cefr_level = get_cefr_level(score)

                # 5.2 Sending Email
                candidate_info = {
                    'name': name,
                    'phone': phone,
                    'language': language
                }

                analysis_results = {
                    'score': score,
                    'cefr_level': cefr_level,
                    'transcript': analysis['transcript']
                }

                email_sent = send_application_email(
                    recipient_email=DEFAULT_RECIPIENT,
                    candidate_info=candidate_info,
                    analysis_results=analysis_results,
                    resume_file=resume,
                    audio_file=temp_audio_path
                )

                if email_sent:
                    st.success("Your application has been submitted successfully.")
                    st.balloons()

                    # Display Results to User
                    st.write(f"**Analysis Result for {name}:**")
                    st.write(f"Proficiency Score: {score}/100")
                    st.write(f"CEFR Level: {cefr_level}")
                    st.write(f"Transcript: {analysis['transcript']}")
                else:
                    st.error("Failed to send application email. Please check server logs.")

                # Clean up unique temp file
                if os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
