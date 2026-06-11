from pathlib import Path
import re, sys

def needs_fullstop(question_block):
    lines = question_block.split("<br/>")

    # Check the first few lines of the question stem
    for line in lines[:5]:

        if re.search(r'=\s*\\\)\s*$', line):
            return True

        text = re.sub(r'<.*?>', '', line).strip()

        if text.endswith("is") or text.endswith("are"):
            return True

    return False


def add_fullstops(question_block):
    lines = question_block.split("<br/>")
    new_lines = []

    for line in lines:
        print("line ", line)
        m = re.match(r'(\s*[A-E]\.\s*)(.*)', line)

        if m:
            prefix, content = m.groups()
            content = content.rstrip()

            if content and not content.endswith("."):
                line = prefix + content + "."

        new_lines.append(line)
    print(new_lines)
    return "<br/>".join(new_lines)


def process_html(html):
    pattern = re.compile(r"<div>(.*?)</div>", re.S)

    def replace_block(match):
        block = match.group(1)

        if needs_fullstop(block):
            block = add_fullstops(block)

        return f"<div>{block}\n</div>"

    return pattern.sub(replace_block, html)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: ./parse pdf_path output_path")
    else:
        input_path, output_path = sys.argv[1], sys.argv[2]
        html = open(input_path).read()
        parsed = process_html(html)
        with open(output_path, "w") as f:
            f.write(parsed)