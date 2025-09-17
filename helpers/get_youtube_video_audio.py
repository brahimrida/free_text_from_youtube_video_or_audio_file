import os
import subprocess

from pytubefix import YouTube


def get_youtube_video_audio(link, out_file="audio.wav") -> str or None:
    yt = YouTube(link)
    audio_stream = yt.streams.filter(only_audio=True).first()
    temp_file = audio_stream.download(filename="temp_audio")  # keeps original extension
    saved_audio_dir = "saved_audio/"
    full_out_file_path = saved_audio_dir + out_file
    if temp_file is None:
        return None
    # convert to mono 16kHz wav using ffmpeg
    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", temp_file,
        "-ac", "1",  # mono
        "-ar", "16000",  # 16kHz
        full_out_file_path
    ], check=True)

    # remove temp file
    os.remove(temp_file)
    return full_out_file_path
