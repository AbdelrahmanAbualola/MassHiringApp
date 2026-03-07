import streamlit as st
from transformers import pipeline
import torch

# Use a lightweight text-generation or summarization model
# For multiple languages, a multilingual model like mBART or a small T5 might be good.
# For simplicity and versatility, we'll use a small multilingual text-to-text model.
MODEL_NAME = "google/flan-t5-small"

@st.cache_resource
def load_summary_pipeline():
    """
    Load and cache the text generation pipeline.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return pipeline("text2text-generation", model=MODEL_NAME, device=device)

def generate_introduction(cv_text, language="English"):
    """
    Generates a summary paragraph for 'Introduce yourself' based on CV text in the selected language.
    """
    if not cv_text:
        return "Please upload a valid CV to generate an introduction."

    try:
        summarizer = load_summary_pipeline()

        # Construct a prompt based on the CV text and desired language
        prompt = f"Based on the following CV, generate a short 'Introduce yourself' paragraph (3-4 sentences) in {language}: \n\n{cv_text[:1000]}"

        # Generate the introduction
        result = summarizer(prompt, max_length=150, min_length=30, do_sample=False)

        intro_text = result[0]['generated_text']

        # Note: Flan-T5 is good at following instructions but might need specific prompting
        # for translation if the CV is in a different language than requested.
        # In a real production app, a larger model or a specialized translation-summarization
        # chain would be used.

        return intro_text
    except Exception as e:
        print(f"Error generating introduction: {e}")
        return "Could not generate introduction. Please provide a brief intro manually."
