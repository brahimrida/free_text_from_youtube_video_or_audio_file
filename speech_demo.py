import os
import sys
import torch
from transformers import (WhisperProcessor, WhisperForConditionalGeneration)
from helpers.audio_chunks_transcriber import transcribe_chunks
from helpers.audio_splitter import split_audio_ffmpeg
from helpers.error_message import error_message, args_missing_count
from helpers.get_youtube_video_audio import get_youtube_video_audio

device = "cuda:0" if torch.cuda.is_available() else "cpu"

USAGE = """
usage:
python speech_demo.py <Youtube video link or audio file path> <flag> <chunks-output-directory-path>
full command example for youtube video text: 
python speech_demo.py https://youtu.be/LzInU71ljJQ?si=_xxxLVIdNDvfBT8d -y C:/path-to-folder/chunks/
full command example for remote/local audio text: 
python speech_demo.py C:/path-to-audio/audio-file.wav OR https//:www.example.com/audio.wav -u C:/path-to-folder/chunks/
flags: 
-y | for youtube link
-u | for audio path
"""


if __name__ == "__main__":
    number_of_args = len(sys.argv)
    if number_of_args != 4:
        left = args_missing_count(number_of_args)
        error_message(f"You are missing {left} arguments", USAGE)
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
        error_message(f"the flag {flag} should be one of these two [-y | -u]", USAGE)
        sys.exit(1)

    # Load Whisper Model
    whisper_model_name = "openai/whisper-tiny"  # small, multilingual
    whisper_processor = WhisperProcessor.from_pretrained(whisper_model_name)
    whisper_model = WhisperForConditionalGeneration.from_pretrained(whisper_model_name).to(device)

    split_audio_ffmpeg(input_file=url, output_dir=audio_chunks_path)
    generated_output = transcribe_chunks(chunks_dir=audio_chunks_path, model=whisper_model, processor=whisper_processor)
    print("full generated text:\n")
    print("-" * 40, "START", "-" * 40)
    print(generated_output)
    print("-" * 40, "END", "-" * 40)
    with open("generated_output.txt", "w") as file:
        file.write(generated_output)
        file.close()
