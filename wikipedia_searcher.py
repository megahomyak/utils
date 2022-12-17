import wikipedia

wikipedia.set_lang(input("Enter your language code: "))
print("Now, enter the terms you want to search, each term on a separate line. Upon finishing, emit a line with nothing.")
terms = []
while True:
    s = input()
    if s:
        terms.append(s)
    else:
        break
results = []
for term in terms:
    while True:
        try:
            summary = wikipedia.summary(term)
        except wikipedia.DisambiguationError as e:
            print(f"The term '{term}' is ambiguous. Disambiguate it by entering one of the following terms, or emit an empty line to skip the term:")
            print("\n".join(e.options))
        except wikipedia.PageError:
            print(f"The term '{term}' was not found. Enter the other term as a replacement or emit an empty line to skip the term:")
        else:
            break
        term = input()
    results.append(summary.split("\n")[0])

print("\n### -------------- ###\n")
print("\n\n".join(results))
