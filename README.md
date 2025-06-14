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

# Install english language model: `python -m spacy download en_core_web_sm`

Run the program: `python main.py`

> > > > > > > acc30cbf287f76d38ca4d481c8566b2cbf9ad287
> > > > > > > Google AI API needed: [https://aistudio.google.com/app/apikey]()

    Store as:`GOOGLE_GENAI_API_KEY` in .env file (need to create this yourself)

### Run locally:

Run the program: `python main.py`

    Terminal will prompt user for Youtube video link, provide it

Run `streamlit run app.py` to visualize results

### Next steps:

Find a better model for generating the transcript and summary: all the downstream analysis and validation is dependent on the first layer

Why do we need a dropdown for both video and video summary (streamlit)?

Add an option to run the full analysis from the streamlit frontend (textbox for user to enter the youtube url)
