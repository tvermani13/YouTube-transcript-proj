# from youtube_transcript_api import YouTubeTranscriptApi
# from urllib.parse import urlparse, parse_qs
# import requests

# def get_video_id(youtube_url):
#     """Extract the video ID from the URL"""
#     parsed_url = urlparse(youtube_url)
#     if parsed_url.hostname == 'youtu.be':
#         return parsed_url.path[1:]
#     elif 'v' in parse_qs(parsed_url.query):
#         return parse_qs(parsed_url.query)['v'][0]
#     else:
#         raise ValueError("Invalid YouTube URL")

# def download_transcript(youtube_url, output_file='transcript.txt'):
#     try:
#         video_id = get_video_id(youtube_url)
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)

#         with open(output_file, 'w', encoding='utf-8') as f:
#             for entry in transcript:
#                 f.write(f"{entry['text']}\n")
        
#         print(f"Transcript saved to '{output_file}'")
#     except Exception as e:
#         print(f"Error: {e}")

# download_transcript("https://www.youtube.com/watch?v=AM0eFRihxDw")

# def summarize_with_ollama(text):
#     response = requests.post("http://localhost:11434/api/generate", json={
#         "model": "mistral",
#         "prompt": f"Summarize and analyze the sentiment of this text:\n{text}",
#         "stream": False
#     })
#     return response.json()["response"]

# print(summarize_with_ollama(open("transcript.txt").read()[:1000]))
import hashlib
import os
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
import requests

def get_video_id(youtube_url):
    parsed_url = urlparse(youtube_url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    elif 'v' in parse_qs(parsed_url.query):
        return parse_qs(parsed_url.query)['v'][0]
    else:
        raise ValueError("Invalid YouTube URL")

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return '\n'.join([entry['text'] for entry in transcript])

def summarize_with_ollama(text):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "mistral",
        "prompt": f"Summarize the following YouTube transcript:\n\n{text}",
        "stream": False
    })
    response.raise_for_status()
    return response.json()["response"]

def hash_video_id(video_id):
    return hashlib.sha256(video_id.encode()).hexdigest()[:12]

def process_youtube_video(youtube_url, base_output_dir="videos"):
    try:
        video_id = get_video_id(youtube_url)
        transcript = get_transcript(video_id)
        video_hash = hash_video_id(video_id)
        
        output_dir = os.path.join(base_output_dir, video_hash)
        os.makedirs(output_dir, exist_ok=True)

        transcript_path = os.path.join(output_dir, "transcript.txt")
        summary_path = os.path.join(output_dir, "summary.txt")

        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(transcript)

        print(f"✅ Transcript saved to {transcript_path}")

        summary = summarize_with_ollama(transcript[:3000])  # limit to ~3k chars for safety
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)

        print(f"✅ Summary saved to {summary_path}")

    except Exception as e:
        print(f"❌ Error: {e}")

# === Example usage ===
process_youtube_video("https://www.youtube.com/watch?v=AM0eFRihxDw")
