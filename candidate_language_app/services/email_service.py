import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
DEFAULT_RECIPIENT = os.getenv("RECIPIENT_EMAIL", "abdelrahman.m.abualola@gmail.com")

def send_application_email(recipient_email, candidate_info, analysis_results, resume_file, audio_file):
    """
    Sends a candidate application email with the CV and voice recording.
    """
    try:
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_email
        msg['Subject'] = f"New Candidate Application: {candidate_info['name']}"

        # Email body
        body = f"""
        A new candidate has submitted their application.

        Candidate Name: {candidate_info['name']}
        Phone Number: {candidate_info['phone']}
        Applied Language: {candidate_info['language']}

        AI-Generated Introduction (Read by candidate):
        {candidate_info['ai_summary']}

        Recording Transcript:
        {analysis_results['transcript']}
        """

        msg.attach(MIMEText(body, 'plain'))

        # Attach Resume
        if resume_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(resume_file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={resume_file.name}")
            msg.attach(part)

        # Attach Voice Recording
        if audio_file:
            with open(audio_file, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(audio_file)}")
                msg.attach(part)

        # Send Email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, recipient_email, text)
        server.quit()

        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
