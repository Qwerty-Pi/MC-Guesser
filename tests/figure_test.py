import re
import json

"""
(Help) checks whether the figure are referenced correctly.
"""

def findFigureInHTML(paper):
    questions = open(f"../artifact/{paper}/questions.html").read()
    pattern = re.compile(r"figures/([0-9a-z]+)\.svg")
    return pattern.findall(questions)

def findFigureInJSON(paper):
    figures = json.loads(open(f"../artifact/{paper}/figures.json").read())
    return [str(fig['label']) for fig in figures]

def compareFigures(paper):
    figures_html = findFigureInHTML(paper)
    figures_json = findFigureInJSON(paper)
    for fig in figures_html:
        if fig not in figures_json:
            print(f"Paper {paper} HTML but not JSON: Figure {fig}")
    for fig in figures_json:
        if fig not in figures_html:
            print(f"Paper {paper} JSON but not HTML: Figure {fig}")

for year in list(range(1980, 2026)) + ["2012-SP", "2012-PP"]:
    compareFigures(f"paper-2/{year}")
