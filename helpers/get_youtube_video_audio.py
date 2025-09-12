import os
import subprocess

from pytubefix import YouTube


def get_youtube_video_audio(link, out_file="audio.wav") -> str or None:
    yt = YouTube(link)
    audio_stream = yt.streams.filter(only_audio=True).first()
    temp_file = audio_stream.download(filename="temp_audio")  # keeps original extension
    if temp_file is None:
        print("Failed to download youtube audio")
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
