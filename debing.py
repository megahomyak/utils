import subprocess

prompt = input("Input prompt: ")
response = u"\u00AD".join(prompt)

output = subprocess.Popen(
    ("xclip", "-selection", "clipboard", "-t", "text/plain", "-i"),
    stdin=subprocess.PIPE,
)
output.stdin.write(response.encode("utf-8"))
output.stdin.close()
output.wait()
