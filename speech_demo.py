import sys
import torch
from pytubefix import YouTube
from transformers import (WhisperProcessor, WhisperForConditionalGeneration)

from helpers.transcript_long_audio import *

device = "cuda:0" if torch.cuda.is_available() else "cpu"


# ---------------------------
# Load Whisper Model
# ---------------------------
whisper_model_name = "openai/whisper-tiny"  # small, multilingual
whisper_processor = WhisperProcessor.from_pretrained(whisper_model_name)
whisper_model = WhisperForConditionalGeneration.from_pretrained(whisper_model_name).to(device)


def get_youtube_video_audio(link, out_file="audio.wav") -> str or None:
    yt = YouTube(link)
    audio_stream = yt.streams.filter(only_audio=True).first()
    temp_file = audio_stream.download(filename="temp_audio")  # keeps original extension
    if temp_file is None:
        print("null file")
        return None
    # convert to mono 16kHz wav using ffmpeg
    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", temp_file,
        "-ac", "1",  # mono
        "-ar", "16000",  # 16kHz
        out_file
    ], check=True)

    # remove temp file
    os.remove(temp_file)
    return out_file


def load_audio(audio_path):
    """Load audio file and resample to 16kHz"""
    speech, sr = torchaudio.load(audio_path)
    # If stereo, convert to mono by averaging channels
    if speech.shape[0] > 1:
        speech = speech.mean(dim=0, keepdim=True)
    resampler = torchaudio.transforms.Resample(sr, 16000)
    speech = resampler(speech)
    return speech.squeeze()

def get_transcription_whisper(audio_path, model, processor, language="english"):
    speech = load_audio(audio_path)
    input_features = processor(
        speech, return_tensors="pt", sampling_rate=16000
    ).input_features.to(device)
    forced_decoder_ids = processor.get_decoder_prompt_ids(
        language=language, task="transcribe"
    )
    predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    return transcription

# ---------------------------
# Demo
# ---------------------------


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("""
        usage: python speech_demo.py <Youtube video link or audio file path> <flag> <chunks-output-directory-path>
        flags: 
        -y | for youtube link
        -u | for local & remote paths
        """)
        sys.exit(1)

    url = sys.argv[1]
    flag = sys.argv[2]
    audio_chunks_path = sys.argv[3]

    if flag == "-y":
        audio_url = get_youtube_video_audio(url)
        if audio_url is None:
            sys.exit(1)
    elif flag == "-u":
        audio_url = url
    else:
        sys.exit(1)

    # print("Running Wav2Vec2...")
    # print(get_transcription_wav2vec2(audio_url, wav2vec2_model, wav2vec2_processor))

    split_audio_ffmpeg(input_file=url, output_dir=audio_chunks_path)
    generated_output = transcribe_chunks(chunks_dir=audio_chunks_path, model=whisper_model, processor=whisper_processor)
    print("full generated text:\n")
    print("-" * 40, "START", "-" * 40)
    print(generated_output)
    print("-" * 40, "END", "-" * 40)

