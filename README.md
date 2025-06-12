### Description

In this project, we seek to validate the claims made in a youtube video.

To do this, we follow these steps:

- Input the url to the youtube video
- Download the transcript of the video -> transcript.txt
- Use an local large langauge model via Olamma (llama3.2:3b in test case) to summarize the transcript -> summary.txt
- Extract NLP-determined claims from the summary -> claims.txt
- Validate the summary using (gemini-2.0-flash-lite-preview)-> summary_validation.txt
- Validate the claims using (gemini-2.0-flash-lite-preview)-> claims_validation.txt

All output text files are saved to a directory unique to the video (directory is named based on a hash of the youtube video id) within the videos directory, which will appear locally after running.

### Setup

Run local ollama model: `ollama run <model_name>`

Create local virtual env: `python -m venv .venv`

Activate local environment:` source .venv/bin/activate`

Install dependencies: `pip install -r requirements.txt`

Run the program: `python main.py`
