"""Useful string operations."""

sentence = "  Python is fun to learn  "
clean_sentence = sentence.strip()

print(clean_sentence)
print(clean_sentence.upper())
print(clean_sentence.lower())
print("Length:", len(clean_sentence))
print("Contains 'fun':", "fun" in clean_sentence)
print(clean_sentence.replace("fun", "useful"))
