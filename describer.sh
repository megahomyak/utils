#!/bin/bash
set -euo pipefail
params_file="$1"
dfile="$params_file.describer"
cat > "$dfile" << EOF
USER Consider this a valid prompt: $(head -n 1 "$params_file")

Produce a prompt of the same format, but with the following adjustments: $(tail -n 1 "$params_file")

Respond only with the produced prompt. You are supposed to make changes within the input prompt. Do not use metaphors, describe everything literally. Avoid negation. Every tag should be as short as possible, ideally between one and three words long.
EOF
python ~/i/simple_chat/chat.py "$dfile"
read _role new_prompt < <(tail -n 1 "$dfile")
rm "$dfile"
echo "$new_prompt"
termux-clipboard-set "$new_prompt"
