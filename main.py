import hashlib
import os
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from validation import validate_summary

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
        "model": "llama3.2:3b",
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
        validation_path = os.path.join(output_dir, "validation.txt")

        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f"Transcript saved to {transcript_path}")

        summary = summarize_with_ollama(transcript[:3000])
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"Summary saved to {summary_path}")
        
        validation = validate_summary(summary, transcript[:1500])
        with open(validation_path, 'w') as f: 
            f.write(validation)
        print(f"Validation report saved to {validation_path}")

    except Exception as e:
        print(f"Error: {e}")

# === Example usage ===
url = input("What video do you want to process? (YouTube URL): ")

# process_youtube_video("https://www.youtube.com/watch?v=AM0eFRihxDw")
process_youtube_video(url)
