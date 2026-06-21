from google import genai
from google.genai import types
import os, httpx, sys
import json

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

def ask(prompt, model):
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    print(response)
    return response.text

def by_topic(paper):
    print(f"By Topic for {paper}")
    prompt = open("topics_J.json", "r").read() + open("topics_S.json", "r").read()
    prompt = prompt.replace("\n", "").replace("  ", " ").replace("  ", " ").replace("  ", " ")
    prompt += "\nRefers to the above documents, classify the topics listed below, and return as an array of the format J1, S3 where J refers to junior, S refers to senior. The format is [J/S][1-99] where the number is the subtopic of the question, NOT the question label itself. Return in JSON format.\n"
    prompt += open(f"artifact/{paper}/questions.html").read().replace("<br/>", "").replace(" ", "").replace("\n", "")
    res = ask(prompt, model="gemini-3.5-flash")
    return json.loads(res[7:-3])

def write_by_topic(paper):
    path = f"artifact/{paper}/topics.json"
    content = by_topic(paper)
    with open(path, "w") as f:
        f.write(json.dumps(content))

def format_html(paper):
    prompt = open(f"prompt.txt").read()
    prompt += open(f"artifact/{paper}/merged.txt").read()
    prompt = prompt.replace(" ", "")
    res = ask(prompt, model="gemini-3.1-flash-lite")
    return res

def write_html(paper):
    path = f"artifact/{paper}/questions.html"
    content = format_html(paper)
    with open(path, "w") as f:
        f.write(content)

if len(sys.argv) == 3:
    paper = sys.argv[1]
    option = sys.argv[2]

    if option == "topic":
        write_by_topic(paper)
    elif option == "statement":
        write_html(paper)
