def concat(L, R):
    content = ""
    for i in range(L, R + 1):
        content += open(f"text/{i}.txt", "r").read()
    return content

with open("paper-1.txt", "w") as f:
    f.write(concat(1, 24))

with open("paper-2.txt", "w") as f:
    f.write(concat(25, 39))
