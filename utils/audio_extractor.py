import os
import yt_dlp
# pyrefly: ignore [missing-import]
from pydub import AudioSegment


DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok = True)

def download_youtube_audio(url:str)->str:
    print("=======================downloading audio from video===========================")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info["id"]

    output_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp3")

    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Expected output file not found: {output_path}")

    return os.path.abspath(output_path)

# result = download_youtube_audio("https://youtu.be/7AW6ORQLWvU?si=lZWL3FeAXNKqK6SR")
# print(result)

def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    print("\n====================converting downloaded audio into WAV format=========================")
    base, _ = os.path.splitext(input_path)
    output_path = f"{base}.wav"

    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) #16khz
    audio.export(output_path, format="wav")

    return output_path

# result_wav = convert_to_wav(result)
# print(result_wav)


def chunk_audio(input_path: str, chunk_minutes: float ) -> list[str]:
    print("\n========================Creating audio chunks....===================================")
    audio = AudioSegment.from_file(input_path)

    chunk_ms = int(chunk_minutes * 60 * 1000)
    total_ms = len(audio)

    base, ext = os.path.splitext(input_path)
    ext = ext.lstrip(".") or "mp3"

    chunk_paths = []
    for i, start in enumerate(range(0, total_ms, chunk_ms)):
        end = min(start + chunk_ms, total_ms)
        chunk = audio[start:end]

        chunk_path = f"{base}_chunk{i:03d}.{ext}"
        chunk.export(chunk_path, format=ext)
        chunk_paths.append(chunk_path)

    return chunk_paths

# result_chunks = chunk_audio(result_wav)
# print(result_chunks)

def process_input(url: str, chunk_minutes: float =3) -> list[str]:
    result = download_youtube_audio(url)
    result_wav = convert_to_wav(result)
    result_chunks = chunk_audio(result_wav, chunk_minutes)
    # print(f"\n\nCHUNK AUDIO: {result_chunks}")
    return result_chunks


# audio_extractor_result = process_input("https://youtu.be/7AW6ORQLWvU?si=lZWL3FeAXNKqK6SR", 8)
# print(audio_extractor_result)