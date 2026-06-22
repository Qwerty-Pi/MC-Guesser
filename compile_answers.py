import os, json
with open("answers.txt", "r") as f:
    while True:
        line = f.readline()
        if len(line.strip()) == 0:
            break
        content = line.split()
        year, content = content[0], content[1:]
        if year == "PP": year = "2012-PP"
        if year == "SP": year = "2012-SP"
        os.makedirs(f"artifact/paper-2/{year}", exist_ok=True)
        with open(f"artifact/paper-2/{year}/answers.json", "w") as f2:
            f2.write(json.dumps(content))
        print(year, content)