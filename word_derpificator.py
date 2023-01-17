import re

RUSSIAN_VOWELS = "уеыаоэяиюё"
ENGLISH_VOWELS = "aieouy"
VOWELS = RUSSIAN_VOWELS + ENGLISH_VOWELS
print(re.sub(
    rf"[{VOWELS}]+[^{VOWELS}_\s\W]+",
    lambda m: m.group(0)[::-1],
    input("Enter the words: "),
    flags=re.IGNORECASE,
))
