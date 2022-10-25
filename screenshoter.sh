mkdir screenshots 2>/dev/null
while true
do
    read -p "Press Enter to capture a screenshot"
    flameshot gui --path $(pwd)/screenshots
done
