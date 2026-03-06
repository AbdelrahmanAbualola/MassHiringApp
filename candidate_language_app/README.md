# Candidate Language Proficiency Application

This is a Streamlit-based web application designed to collect candidate job applications and evaluate their spoken language proficiency using AI.

## Features
- Candidate information form (Name, Phone, Resume upload).
- Voice recording directly in the browser or via file upload (WAV, MP3, M4A).
- Speech-to-text transcription and proficiency scoring using Hugging Face's OpenAI Whisper model.
- Automated email notifications to recruiters with candidate details and attachments.
- Interactive and user-friendly interface with model caching for performance.

## Project Structure
```text
candidate_language_app/
├── app.py                   # Main Streamlit application
├── services/
│   ├── speech_analysis.py   # Hugging Face transcription and analysis (Cached)
│   └── email_service.py     # Email sending service using smtplib
├── utils/
│   ├── audio_processing.py  # Audio format normalization (16kHz WAV)
│   └── scoring.py           # Proficiency and CEFR scoring logic
├── .env.example             # Example environment variables
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- **ffmpeg** (Required for `pydub` to handle MP3/M4A audio processing).
  - **Linux**: `sudo apt install ffmpeg`
  - **macOS**: `brew install ffmpeg`
  - **Windows**: [Download and install ffmpeg](https://ffmpeg.org/download.html) and add to PATH.

### 2. Clone the Repository
```bash
git clone <repository-url>
cd candidate_language_app
```

### 3. Install Dependencies
Ensure you have Python 3.10+ installed.
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory and add the following:
```env
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
RECIPIENT_EMAIL=abdelrahman.m.abualola@gmail.com
```
*Note: If using Gmail, you may need to generate an [App Password](https://support.google.com/accounts/answer/185833).*

### 5. Run the Application
```bash
streamlit run app.py
```

## How It Works
1. **Form Submission**: The candidate fills in their name, phone number, and uploads a resume.
2. **Language Selection**: The candidate selects the language for the proficiency test.
3. **Voice Recording**: The candidate records a short message or uploads an existing recording.
4. **Speech Analysis**: On submission, the app uses a cached Whisper model to transcribe the audio and calculate a proficiency score based on model confidence and recording duration.
5. **Email Delivery**: An automated email is sent to the recruiter containing the analysis results and the attached resume/recording.
6. **User Feedback**: The candidate receives immediate feedback and their results on the screen.
