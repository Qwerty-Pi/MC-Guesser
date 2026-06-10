from google import genai
from google.genai import types
import os, httpx, sys

def ask(question):
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"], http_options={"timeout": 300_000}) # 5 minutes
    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents=question
    )
    return response.text

paper = "2012-PP"
prompt = f"Can you give me the answer to DSE {paper} Mathematics Paper 2 in array?"
resp = ask(prompt)
print(resp)
