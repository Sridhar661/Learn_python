"""Write to and read from a simple text file."""

file_name = "sample_notes.txt"

with open(file_name, "w", encoding="utf-8") as file:
    file.write("I am practising Python file handling.\n")
    file.write("The with statement closes the file automatically.\n")

with open(file_name, "r", encoding="utf-8") as file:
    contents = file.read()

print(contents)
print(f"Created/read: {file_name}")
