import os
from pydub import AudioSegment
import io
import soundfile as sf
import librosa
import tempfile

def process_audio(audio_data, file_extension):
    """
    Processes audio data (bytes or path) and returns a unique temporary 16kHz mono WAV file path.
    """
    try:
        # Load audio data into pydub AudioSegment
        if isinstance(audio_data, bytes):
            audio = AudioSegment.from_file(io.BytesIO(audio_data), format=file_extension.replace('.', ''))
        else:
            audio = AudioSegment.from_file(audio_data)

        # Normalize audio (convert to mono, 16kHz)
        audio = audio.set_frame_rate(16000).set_channels(1)

        # Export to a unique temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            temp_wav_path = temp_wav.name
            audio.export(temp_wav_path, format="wav")

        return temp_wav_path
    except Exception as e:
        raise Exception(f"Error processing audio: {e}")

def get_audio_duration(file_path):
    """
    Returns the duration of the audio file in seconds.
    """
    try:
        y, sr = librosa.load(file_path, sr=None)
        return librosa.get_duration(y=y, sr=sr)
    except Exception as e:
        print(f"Error calculating duration: {e}")
        return 0
