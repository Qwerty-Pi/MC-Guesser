from google import genai
from google.genai import types
import os, httpx, sys
import json

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

def ask(prompt):
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt
    )
    print(response)
    return response.text

def by_topic(year):
    prompt = open("topics_J.json", "r").read() + open("topics_S.json", "r").read()
    prompt += "\nRefers to the above documents, classify the topics listed below, and return as an array of the format J1, S3 where J refers to junior, S refers to senior. Return in JSON format.\n"
    prompt += open(f"artifact/paper-2/{year}/questions.html").read()
    print(prompt)
    exit(0)
    res = ask(prompt)
    return json.loads(res[7:-3])

def write_by_topic(year):
    path = f"artifact/paper-2/{year}/topics.json"
    content = by_topic(year)
    with open(path, "w") as f:
        f.write(json.dumps(content))

if len(sys.argv) == 2:
    year = sys.argv[1]
    write_by_topic(year)