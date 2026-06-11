# MC Guesser

Sor I commit things to main directly so most things are testing files and stuff. Below is important files.

## File Structure

Stuff marked in (*) are those need manual change
```
raw
|
|-- paper-X
    |
    |-- year.pdf (*)

artifact
|
|--paper-X
    |
    |-- year
        |
        |-- figure/ (generated from figures.json)
        |
        |-- page/ (images of the pages)
        |
        |-- text/ (OCR text for each page separately)
        |
        |-- answers.json (*) (answers to the questions)
        |
        |-- figures.json (*) (specify the figure name + (page, bounding box) in pdf)
        |
        |-- merged.txt (merged OCR text)
        |
        |-- questions.html (*) (Use GPT to change OCR text to HTML)
        |
        |-- questions.json (generated from questions.html - not necessarily? But it works for now)
        |
        |-- topics.json (topics list. Also just GPT it)
```

## Things
- `ask_gemini.py`: Ask gemini. Currently returns a JSON of the topic list using the local compiled html version of the paper. Need Geminin API Key, free quota 20 everyday. Should be sufficient (or if you are rich probably can use other API). 
- `gen_figure`: Generate figures base on `figures.json`. Working mechanism is just for split the pdf into pages and convert the pdf into svg, then use svg `clipbox` to crop the box out (memory might be large? But anyways). Also scaled 1.5x to match the normal 12px in webpage. (Since the original pdf are not all exactly of A4 size, need to first cast the page to A4 first with commands).
- `fix_fullstop.py`: Fix fullstop.
- `parse`: Use `ollama parse` to OCR the text. Using `static OCR` (coz I am poor). Seems you can use LLM to do this with API keys, and there might be other ways to do this as well.
- `prompt.txt`: The prompt I used to make it "kind of works" and give something good enough.
- `topic.html`: Paper By Topic. You can change the topic by clicking on the problem and change the topic. (I am using php local server via `php -S localhost:8000`) Currently is pretty slow, can see see how to fix this (now not using DB coz github.io not support DB, and lazy)
- `year.html`: Paper By Year.
- `topics_[J/S].json`: Just go to EDB website and copy the syllabus and split the pdf. Fun fact is you can `pdftk [file].pdf cat 6-7 output [output].pdf` on linux to cut the pdf and feed to LLM.
- `pdf_cropper.html`: Vibe pdf cropper for loading images. Can download `figures.json`.
- `compile`: Most useful. Elab below.

## Current Method
- Step 1. Obtain the raw paper pdf.
- Step 2. OCR the pdf via `ollama parse` to obtain text.
- Step 3. Throw the text to LLM to obtain a working html (along with the prompt).
- Step 4. Put to `questions.html` and `parse_paper` function in `./compile` will converts it to `questions.json`.
- Step 5. Crop the figures using `pdf_cropper.html`. Download the `figures.json` and put to the directory (actually, `gen_figure` function in `./compile` can copy from the download path, I am using wsl). 
- Step 6. Run `gen_figure` function in `./compile` to actually generate the figures.
- Step 7. Proofread the text. Expect to die a bit. Change the prompt to be more specific if needed.
- Step 8. Use `ask_gemini.py` to ask gemini (or just throw to your favourite LLM). Generate the `topics.json` and put to the directory.

## Improvements
- ollama parse static pretty slow (1.5 min per page). Not like will die but can be better
- Currently need manually throw the text to LLM. How to automate this step so no need manual at all?
- auto crop so no need hand crop?