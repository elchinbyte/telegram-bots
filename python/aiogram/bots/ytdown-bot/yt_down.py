import os, re
from yt_dlp import YoutubeDL
from config import FFMPEG_PATH

def download_video(url: str):
    options = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "ffmpeg_location": FFMPEG_PATH,
        "outtmpl": "downloads/video/%(title)s.%(ext)s",
        "restrictfilenames": True, 
        "quiet": False,
    }

    with YoutubeDL(options) as ydl:
        ydl.download([url])

def download_audio(url: str):
    options = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/audio/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "restrictfilenames": True, 
        "quiet": False,
    }

    with YoutubeDL(options) as ydl:
        ydl.download([url])

def get_latest_file(choice: str) -> str | None:
    folder = os.path.join("downloads", choice)

    if not os.path.exists(folder):
        return None

    files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
    ]

    if not files:
        return None

    latest_file = max(files, key=os.path.getmtime)

    safe_name = re.sub(r"[^\w\.-]", "_", os.path.basename(latest_file))
    safe_path = os.path.join(os.path.dirname(latest_file), safe_name)

    if safe_path != latest_file:
        os.rename(latest_file, safe_path)

    return os.path.abspath(safe_path).replace("\\", "/")