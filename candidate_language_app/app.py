import streamlit as st
import os
import io
import re
from services.speech_analysis import transcribe_audio
from services.cv_summary import generate_introduction
from services.email_service import send_application_email, DEFAULT_RECIPIENT
from utils.audio_processing import process_audio
from utils.cv_parser import parse_cv
from streamlit_mic_recorder import mic_recorder

# Application Configuration
st.set_page_config(page_title="Candidate Job Application Portal", layout="centered")

def validate_phone(phone_number):
    """
    Validates the format of the phone number using a simple regex.
    """
    pattern = r'^\+?[\d\s-]{10,20}$'
    return re.match(pattern, phone_number) is not None

def main():
    st.title("Candidate Application Portal")
    st.markdown("Please complete your application below.")

    # 1. Candidate Information
    with st.container():
        st.subheader("1. Profile Information")
        name = st.text_input("Full Name", placeholder="Enter your full name", key="name")
        phone = st.text_input("Phone Number", placeholder="Enter your phone number (e.g., +1234567890)", key="phone")

        # 2. CV Upload & Language Selection
        st.subheader("2. Experience & Language")
        resume = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"], key="resume")
        language = st.selectbox("Application Language", ["English", "German", "Italian"], key="language")

    # 3. AI Generated Introduction
    generated_intro = ""
    if resume and name:
        with st.status("Analyzing CV and generating your introduction...", expanded=True) as status:
            cv_text = parse_cv(resume)
            if cv_text:
                generated_intro = generate_introduction(cv_text, language=language)
                st.subheader("3. Your AI-Generated Introduction")
                st.info("Please read the following paragraph during your voice recording:")
                st.markdown(f"> {generated_intro}")
                status.update(label="Introduction generated!", state="complete", expanded=False)
            else:
                st.warning("Could not extract text from the uploaded CV. Please ensure it's a valid PDF or DOCX.")
                status.update(label="CV parsing failed.", state="error")

    # 4. Voice Recording
    st.subheader("4. Voice Introduction")
    st.write("Record yourself reading the introduction above.")

    audio_data = None
    recording = mic_recorder(
        start_prompt="Start Recording",
        stop_prompt="Stop Recording",
        just_once=False,
        key="recorder"
    )

    if recording:
        audio_data = recording['bytes']
        st.audio(audio_data, format='audio/wav')

    # 5. Submission
    if st.button("Submit Application", type="primary"):
        # Validation
        if not name:
            st.error("Full Name is required.")
            return
        if not phone or not validate_phone(phone):
            st.error("A valid Phone Number is required.")
            return
        if not resume:
            st.error("Please upload your CV.")
            return
        if not generated_intro:
            st.error("Please ensure your CV is parsed and an introduction is generated.")
            return
        if not audio_data:
            st.error("Please provide a voice recording of your introduction.")
            return

        with st.spinner("Submitting your application..."):
            temp_audio_path = None
            try:
                # Process audio
                temp_audio_path = process_audio(audio_data, 'wav')

                # Transcribe recording
                analysis = transcribe_audio(temp_audio_path, language=language)

                # Ensure the file pointer for the resume is reset before reading it for the email
                resume.seek(0)

                # Send Email
                candidate_info = {
                    'name': name,
                    'phone': phone,
                    'language': language,
                    'ai_summary': generated_intro
                }

                analysis_results = {
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
                else:
                    st.error("Failed to send application email. Please try again later.")

            except Exception as e:
                st.error(f"An error occurred during submission: {e}")
            finally:
                if temp_audio_path and os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)

if __name__ == "__main__":
    main()
