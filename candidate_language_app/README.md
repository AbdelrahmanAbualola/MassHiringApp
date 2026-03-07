# Candidate Job Application Portal

A Streamlit-based web application for job candidates to apply, featuring AI-generated personal introductions based on their CVs.

## Features
- **Candidate Form**: Collects name, phone number, and CV.
- **CV Analysis**: Parses uploaded PDF/DOCX files and extracts text.
- **AI Introduction**: Automatically generates a "Introduce yourself" summary paragraph in the selected language (English, German, or Italian) based on the candidate's CV.
- **Voice Recording**: Candidates record themselves reading the AI-generated introduction.
- **Automated Notification**: Sends an email to recruiters with candidate details, the AI summary, the recording transcription, and all attachments.

## Project Structure
```text
candidate_language_app/
├── app.py                   # Main Streamlit application
├── services/
│   ├── cv_summary.py        # AI logic for generating introductions
│   ├── speech_analysis.py   # Transcription logic using OpenAI Whisper
│   └── email_service.py     # Email notification logic
├── utils/
│   ├── audio_processing.py  # Audio normalization
│   └── cv_parser.py         # PDF/DOCX text extraction
├── packages.txt             # System-level dependencies (ffmpeg)
├── requirements.txt         # Python dependencies
└── README.md                # Documentation
```

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- **ffmpeg** (Required for audio processing).

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root with your SMTP credentials:
```env
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
RECIPIENT_EMAIL=abdelrahman.m.abualola@gmail.com
```

### 4. Run
```bash
streamlit run app.py
```

## AI Models Used
- **CV Summarization**: `google/flan-t5-small` via Hugging Face.
- **Speech-to-Text**: `openai/whisper-small` via Hugging Face.
