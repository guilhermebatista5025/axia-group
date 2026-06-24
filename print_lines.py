with open(r"c:\Users\Aluno\Downloads\axia-group\assets\css\styles.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(149, 220):
    if i < len(lines):
        print(f"Line {i+1}: {lines[i]}", end="")
