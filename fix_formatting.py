from pathlib import Path
import re, sys

def fix_fullstop(question):
    lines_parsed = []
    lines = question.split("<br/>") 
    ended_with_punctuation = False
    for line in lines:
        line = line.strip()

        option = re.match(r'([A-E]\.\s*)(.*)', line)
        item = re.match(r'^(I|II|III|IV)\.', line)
        figure = re.match(r'<img.*>', line)
        equation = re.match(r'\\\[.*\\\]', line)
        if option:
            prefix, content = option.groups()
            prefix = prefix.strip()
            content = content.strip()
            match = re.fullmatch(r"((-|\d|\\,)+(\.\d+)?)\.?(.*)", content)
            if match:
                content = r"\(" + match.group(1) + r"\)" + match.group(4)
            line = f"{prefix} {content}"
            should_end = False
            if ended_with_punctuation:
                if len(content) > 20 and not content.startswith("\\("):
                    should_end = True
            else:
                should_end = True
            # should_end = False # old paper doesn't have!
            # should not add fullstop to figures!
            if re.match(r'<img.*>', content):
                should_end = False
            if should_end and not line.endswith("."):
                line += "."
            if not should_end and line.endswith("."):
                line = line[:-1]
        elif figure:
            pass
        elif item:
            pass
        elif equation:
            pass
        else:
            ended_with_punctuation = line.endswith(".") or line.endswith("?") # or line.endswith(r"\)")
        if line.strip() == "":
            continue # do not add empty <br>
        lines_parsed.append(line)
    return "<br/>\n".join(lines_parsed)

def fix_numeric_string(text):
    pattern = re.compile(r"([^.\dA-F])(\d+)(\d\d\d)")
    def replace(match):
        b = [match.group(g) for g in [1, 2, 3]]
        return b[0] + b[1] + "\\," + b[2] # spacing
    return pattern.sub(replace, text)

def fix_arb(text):
    text = text.replace("<br>", "<br/>")
    text = text.replace(r"\text{cm}", "\\text{ cm}") \
               .replace(r"\text{kg}", "\\text{ kg}") \
               .replace(r"\text{marks}", r"\text{ marks}")
    text = text.replace(r"\widehat", r"\overparen")
    text = text.replace(r".\)", r"\)")
    return text

def fix_cmp(text):
    math_mode = re.compile(r"\\\((.*?)\\\)")
    def replace_cmp(match):
        content = match.group(1)
        content = content.replace("<", r" \lt ")
        content = content.replace(">", r" \gt ")
        return r"\(" + content + r"\)"
    return math_mode.sub(replace_cmp, text)

def fix_numbers(text):
    text = re.sub(r"(\d+)\\\(\\text", r"\( \1 \\text", text)
    text = re.sub(r"([\d\\,]+)\\\(\\pi", r"\( \1 \\pi", text)
    text = re.sub(r"([\d.]+)%", r"\( \1 \% \)", text)
    text = re.sub(r"\$((\d|\.|\\,)+)", r"\( \$ \1 \)", text)
    text = re.sub(r"([A-Za-df-z])(\s?)(\d+)(\s[A-Za-z]|\.)", r"\1\2\( \3 \)\4", text)
    return text

def format_question(text):
    text = fix_fullstop(text)
    text = fix_numeric_string(text)
    text = fix_arb(text)
    text = fix_cmp(text)
    text = fix_numbers(text)
    text = text.replace("figures/figure", "figures/")
    return text

def format_paper(text):
    text = text.strip('`\n') # strip off rubbish
    pattern = re.compile(r"<div>(.*?)</div>", re.S)
    result = pattern.sub(lambda div: f"<div>{format_question(div.group(1))}\n</div>", text)
    return result

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 fix_fullstop.py input_path output_path")
    else:
        input_path, output_path = sys.argv[1], sys.argv[2]
        html = open(input_path).read()
        parsed = format_paper(html)
        with open(output_path, "w") as f:
            f.write(parsed)
