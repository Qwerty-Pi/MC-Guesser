from google import genai
from google.genai import types
import os, httpx, sys

def ask(question):
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"], http_options={"timeout": 300_000}) # 5 minutes
    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents=question
    )
    print("Wait for responses...")
    res = response.text
    for candidate in response.candidates:
        finish_reason = candidate.finish_reason
        print(f"Finish Reason: {finish_reason}")
        
        # Check if generation was cut off due to token limits
        if finish_reason == "MAX_TOKENS":
            print("Warning: Response was truncated because it reached max_output_tokens limit.")
    return res

prompt = open("prompt.txt", "r").read() + open("artifact/paper-2/2012-PP/merged.txt", "r").read()
resp = ask(prompt)
print(resp)
