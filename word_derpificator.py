import re

VOWELS = "aieouy"
print(re.sub(
    rf"[{VOWELS}]+[^{VOWELS}_\s\W]+",
    lambda m: m.group(0)[::-1],
    input("Enter the words: "),
    flags=re.IGNORECASE,
))
