import os
import subprocess


def split_audio_ffmpeg(input_file: str, output_dir: str, chunk_length: int = 10):
    """
    Split audio into N-second chunks using ffmpeg and store them in output_dir.
    """
    print("\nSplitting audio...")
    # deleting old files if exists to avoid processing them with the ones we actually need.
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        "ffmpeg", "-i", input_file,
        "-f", "segment",
        "-segment_time", str(chunk_length),
        "-c", "copy",
        os.path.join(output_dir, "chunk_%03d.wav")
    ]
    subprocess.run(cmd, check=True)
    print("\nDone splitting")
