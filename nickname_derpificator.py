import re

def process_word(word):
    return re.sub(
        r"[aieouy]+[^aieouy]+",
        lambda m: m.group(0)[::-1],
        word,
        flags=re.IGNORECASE,
    )

nickname = input("Enter a nickname: ")

print(" ".join(process_word(word) for word in nickname.split()))
