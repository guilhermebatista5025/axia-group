with open(r"c:\Users\Aluno\Downloads\axia-group\assets\css\styles.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if ".header" in line:
        print(f"Line {i+1}: {line.strip()}")
