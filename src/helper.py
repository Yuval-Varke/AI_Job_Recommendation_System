import fitz
import os 
from dotenv import load_dotenv
load_dotenv()
from google import genai
from google.genai import types


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)


def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file.
    
    Args:
        uploaded_file (str): The path to the PDF file.
        
    Returns:
        str: The extracted text.
    """

    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text



def ask_gemini(prompt, max_tokens=2000, max_continuations=2):
    """
    Sends a prompt to the Gemini API and returns the response.

    Args:
        prompt (str): The prompt to send to the Gemini API.
        model (str): The model to use for the request.
        temperature (float): The temperature for the response.
        
    Returns:
        str: The response from the Gemini API.
    """
    
    contents = [prompt]
    full_text = ""
    continuations_used = 0

    while True:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=max_tokens,
            ),
        )

        if not response.text:
            break

        full_text += response.text

        finish_reason = None
        if response.candidates:
            finish_reason = response.candidates[0].finish_reason

        if str(finish_reason).upper().endswith("MAX_TOKENS") and continuations_used < max_continuations:
            # Ask the model to continue using a short follow-up turn.
            contents = [
                prompt,
                response.text,
                "Continue from where you left off. Do not repeat content.",
            ]
            continuations_used += 1
            continue

        break

    return full_text
