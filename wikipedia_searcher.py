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
    results.append(wikipedia.summary(term).split("\n")[0])

print("\n\n".join(results))
