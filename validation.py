import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_GENAI_API_KEY")

genai.configure(api_key=api_key)

# Fetch the list of available models
available_models = genai.list_models()
# for model in available_models:
#     print(model)
# Update the model to a valid one (replace 'gemini-pro' with a valid model name)
model = genai.GenerativeModel("gemini-2.0-flash-lite-preview")

def validate_summary(summary, transcript_excerpt):
    prompt = f"""
    Please fact-check the following summary of a YouTube video using up-to-date internet sources.
    
    --- BEGIN SUMMARY ---
    {summary}
    --- END SUMMARY ---

    --- CONTEXT (optional excerpt from transcript) ---
    {transcript_excerpt}
    --- END CONTEXT ---

    1. Are there any factual errors or outdated claims?
    2. Are there parts that need clarification?
    3. If possible, list corrected or verified facts.

    Provide a bullet-point validation report with citations if available.
    """
    response = model.generate_content(prompt)
    return response.text
