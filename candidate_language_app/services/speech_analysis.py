import torch
from transformers import pipeline
import streamlit as st
import os

# Use OpenAI's Whisper model (e.g., whisper-small)
MODEL_NAME = "openai/whisper-small"

@st.cache_resource
def load_transcription_pipeline():
    """
    Load and cache the Whisper transcription pipeline.
    This prevents the model from being reloaded on every run/request.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return pipeline("automatic-speech-recognition", model=MODEL_NAME, device=device)

def transcribe_audio(audio_path, language="English"):
    """
    Transcribe the audio at the given path using the cached Whisper pipeline.
    Returns the transcription text.
    """
    try:
        asr_pipeline = load_transcription_pipeline()

        # Provide language hint if applicable
        generate_kwargs = {"language": language.lower()} if language else {}

        result = asr_pipeline(audio_path, generate_kwargs=generate_kwargs)

        return {
            "transcript": result["text"]
        }
    except Exception as e:
        print(f"Error during transcription: {e}")
        return {
            "transcript": "Transcription failed."
        }
