from google import genai
from google.genai import types
import os, httpx, sys

def ask(question):
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"], http_options={"timeout": 300_000}) # 5 minutes
    response_stream = client.models.generate_content_stream(
        model='gemini-flash-latest',
        contents=question
    )
    print("Wait for responses...")
    res = ""
    for chunk in response_stream:
        res += chunk.text
        sys.stdout.write(chunk.text)
        sys.stdout.flush()
    return res

os.system("cat prompt.txt text/{25-}.txt > actual-prompt.txt")
prompt = open("actual-prompt.txt", "r").read()
resp = ask(prompt)
print(resp)
