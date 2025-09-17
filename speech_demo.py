import os
import sys
import torch
from transformers import (WhisperProcessor, WhisperForConditionalGeneration)
from helpers.audio_chunks_transcriber import transcribe_chunks
from helpers.audio_splitter import split_audio_ffmpeg
from helpers.download_youtube_video import download_youtube_video
from helpers.error_message import error_message, args_missing_count
from helpers.get_youtube_video_audio import get_youtube_video_audio

device = "cuda:0" if torch.cuda.is_available() else "cpu"

USAGE = """
usage:
python speech_demo.py <Youtube video link or audio file path> <flag>
full command example for youtube video text:
python speech_demo.py https://youtu.be/LzInU71ljJQ?si=_xxxLVIdNDvfBT8d -y
full command example for remote/local audio text:
python speech_demo.py C:/path-to-audio/audio-file.wav OR https//:www.example.com/audio.wav -u
full command example for only youtube video:
python speech_demo.py https://youtu.be/LzInU71ljJQ?si=_xxxLVIdNDvfBT8d -v
flags: 
-y | to get text from youtube video
-u | to get text from local/remote audio
-v | to download youtube video
"""
ACCEPTED_FLAGS = ["-v", "-y", "-u"]

if __name__ == "__main__":
    number_of_args = len(sys.argv)

    if number_of_args != 3:
        error_message(f"You should pass 3 arguments", USAGE)
        sys.exit(1)

    url = sys.argv[1]
    flag = sys.argv[2]

    if flag not in ACCEPTED_FLAGS:
        error_message("wrong flag, must be one of the 3 [ -y | -u | -v ]", USAGE)
        sys.exit(1)

    if flag == "-v":
        audio_url = download_youtube_video(url)
        if audio_url is None:
            print("download wasn't successful")
            sys.exit(1)
        print("-" * 40, "INFO", "-" * 40)
        print("Video was saved successfully")
        print("-" * 40, "INFO", "-" * 40)
        sys.exit(1)
    elif flag == "-y":
        audio_url = get_youtube_video_audio(url)
        if audio_url is None:
            print("download wasn't successful")
            sys.exit(1)
    else:
        audio_url = url

    # Load Whisper Model
    whisper_model_name = "openai/whisper-tiny"  # small, multilingual
    whisper_processor = WhisperProcessor.from_pretrained(whisper_model_name)
    whisper_model = WhisperForConditionalGeneration.from_pretrained(whisper_model_name).to(device)
    split_audio_ffmpeg(input_file=audio_url, output_dir="chunks/")
    generated_output = transcribe_chunks(chunks_dir="chunks/", model=whisper_model,
                                         processor=whisper_processor)
    print("full generated text:\n")
    print("-" * 40, "START", "-" * 40)
    print(generated_output)
    print("-" * 40, "END", "-" * 40)
    with open("generated_output.txt", "w") as file:
        file.write(generated_output)
        file.close()
