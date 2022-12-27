import re

def process_word(word):
    return re.sub(
        r"[aieouy]+[^aieouy]+",
        lambda m: m.group(0)[::-1],
        word,
        flags=re.IGNORECASE,
    )

words = input("Enter the words: ")

print(" ".join(process_word(word) for word in words.split()))
