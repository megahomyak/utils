#!/bin/bash
set -euo pipefail
params_file="$1"
dfile="$params_file.describer"
cat > "$dfile" << EOF
USER Consider this a valid prompt: $(head -n 1 "$params_file")

Produce a prompt of the same format, but with the following adjustments: $(tail -n 1 "$params_file")

Respond only with the produced prompt.
EOF
python ~/i/simple_chat/chat.py "$dfile"
read _role new_prompt < <(tail -n 1 "$dfile")
rm "$dfile"
termux-clipboard-set "$new_prompt"
