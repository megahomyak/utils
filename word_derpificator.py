import re

print(re.sub(
    r"[aieouy]+[^aieouy\s]+",
    lambda m: m.group(0)[::-1],
    input("Enter a nickname: "),
    flags=re.IGNORECASE,
))
