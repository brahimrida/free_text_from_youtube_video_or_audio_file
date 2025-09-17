import os
import subprocess
from typing import Optional
from pytubefix import YouTube


def download_youtube_video(link) -> Optional[str]:
    vid_name = "downloaded_youtube_video.mp4"
    aud_name = "downloaded_youtube_audio.mp3"
    saved_video_dir = "saved_video/"
    yt = YouTube(link)

    video_stream = yt.streams.filter(res="1080p", only_video=True).first()
    audio_stream = yt.streams.filter(only_audio=True).first()

    video_path = video_stream.download(filename=vid_name)  # keeps original extension
    audio_path = audio_stream.download(filename=aud_name)  # keeps original extension

    if video_path is None or audio_path is None:
        print("Failed to download youtube video")
        return None

    combined_file = saved_video_dir + "full_video.mp4"

    cmd = [
        "ffmpeg",
        "-i", video_path,  # your video file (no audio, or with audio you want to replace)
        "-i", audio_path,  # your audio file
        "-c:v", "copy",  # copy video stream without re-encoding
        "-c:a", "aac",  # encode audio to AAC (most compatible)
        "-shortest",  # stop when the shorter stream ends
        combined_file  # final file
    ]
    subprocess.run(cmd, check=True)
    os.remove(vid_name)
    os.remove(aud_name)

    return combined_file
