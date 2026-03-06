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
    # return pipeline("automatic-speech-recognition", model=MODEL_NAME, chunk_length_s=30, device=device)
    # Using small model for demo, it also has better compatibility with some versions
    return pipeline("automatic-speech-recognition", model=MODEL_NAME, device=device)

def transcribe_audio(audio_path, language="English"):
    """
    Transcribe the audio at the given path using the cached Whisper pipeline.
    Returns transcription and confidence scores.
    """
    try:
        asr_pipeline = load_transcription_pipeline()

        # Provide language hint if applicable
        generate_kwargs = {"language": language.lower(), "return_timestamps": True} if language else {"return_timestamps": True}

        result = asr_pipeline(audio_path, generate_kwargs=generate_kwargs)

        # Result typically includes "text" and "chunks"
        transcript = result["text"]

        # Whisper pipeline doesn't directly return a per-utterance "confidence" in the same way
        # as some other models. For a real production app, we would use the model directly with
        # return_dict_in_generate=True, output_scores=True.
        # For this version, we'll estimate confidence based on the presence of words and timestamps.

        chunks = result.get('chunks', [])
        # Simple heuristic: longer and more chunks with timestamps suggest better recognition
        num_chunks = len(chunks)
        confidence = 0.9 if num_chunks > 0 else 0.5

        return {
            "transcript": transcript,
            "confidence": confidence
        }
    except Exception as e:
        print(f"Error during transcription: {e}")
        return {
            "transcript": "Transcription failed.",
            "confidence": 0.0
        }
