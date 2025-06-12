import os
from dotenv import load_dotenv
import google.generativeai as genai
import spacy

load_dotenv()

api_key = os.getenv("GOOGLE_GENAI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash-lite-preview")

nlp = spacy.load("en_core_web_sm")

def extract_claims(summary_text):
    doc = nlp(summary_text)
    claims = []

    for sent in doc.sents:
        if sent.text.strip() == "":
            continue

        # Heuristic: factual claim = sentence with a subject + verb and no question mark
        if sent[-1].text != "?" and any(tok.dep_ == "nsubj" for tok in sent) and any(tok.pos_ == "VERB" for tok in sent):
            claims.append(sent.text.strip())

    return claims

def validate_summary(summary, transcript_excerpt):
    prompt = f"""
    Fact-check the following summary of a transcript of a YouTube video using up-to-date sources.
    
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



def validate_claims_with_gemini(claims):
    prompt = f"""
Validate the following factual claims using real-time and accurate sources.

For each claim:
1. State whether it is true, false, or unverifiable.
2. Provide corrections if applicable.
3. Add citations if possible.

Claims:
{chr(10).join([f"- {c}" for c in claims])}
"""
    response = model.generate_content(prompt)
    return response.text
