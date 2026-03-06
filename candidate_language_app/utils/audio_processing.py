import os
from pydub import AudioSegment
import io
import soundfile as sf
import librosa
import tempfile
import numpy as np

def process_audio(audio_data, file_extension):
    """
    Processes audio data (bytes or path) and returns a unique temporary 16kHz mono WAV file path.
    """
    temp_wav_path = None
    try:
        # Normalize file extension
        ext = file_extension.lower().replace('.', '')

        # Try using pydub first
        try:
            if isinstance(audio_data, bytes):
                audio = AudioSegment.from_file(io.BytesIO(audio_data), format=ext)
            else:
                audio = AudioSegment.from_file(audio_data)

            # Normalize audio (convert to mono, 16kHz)
            audio = audio.set_frame_rate(16000).set_channels(1)

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
                temp_wav_path = temp_wav.name
                audio.export(temp_wav_path, format="wav")
            return temp_wav_path

        except Exception as pydub_err:
            print(f"Pydub failed: {pydub_err}. Trying soundfile/librosa fallback for WAV/FLAC.")

            # Fallback for WAV using soundfile/librosa (doesn't require ffmpeg)
            if ext in ['wav', 'flac']:
                if isinstance(audio_data, bytes):
                    data, samplerate = sf.read(io.BytesIO(audio_data))
                else:
                    data, samplerate = sf.read(audio_data)

                # Convert to mono if stereo
                if len(data.shape) > 1:
                    data = np.mean(data, axis=1)

                # Resample to 16kHz if necessary
                if samplerate != 16000:
                    data = librosa.resample(data, orig_sr=samplerate, target_sr=16000)

                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
                    temp_wav_path = temp_wav.name
                    sf.write(temp_wav_path, data, 16000)
                return temp_wav_path
            else:
                # If it's MP3/M4A and pydub failed (likely missing ffmpeg), we can't do much without ffmpeg
                raise Exception(f"Failed to process {ext} file. ffmpeg might be missing. Error: {pydub_err}")

    except Exception as e:
        if temp_wav_path and os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)
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
