import re

print(re.sub(
    r"[aieouy]+[^aieouy_\s\W]+",
    lambda m: m.group(0)[::-1],
    input("Enter the words: "),
    flags=re.IGNORECASE,
))
