import torchaudio


def load_audio(audio_path):
    """Load audio file and resample to 16kHz"""
    speech, sr = torchaudio.load(audio_path)
    # If stereo, convert to mono by averaging channels
    if speech.shape[0] > 1:
        speech = speech.mean(dim=0, keepdim=True)
    resampler = torchaudio.transforms.Resample(sr, 16000)
    speech = resampler(speech)
    return speech.squeeze()