#!/usr/bin/python

import re
import subprocess
import os
DEVICE_NAME = "AT Translated Set 2 keyboard"
device_info = subprocess.run(["xinput", "list", DEVICE_NAME], stdout=subprocess.PIPE).stdout.decode()
first_line = device_info.split("\n")[0]
match_ = re.match(r".+id=(\d+)\s+\[slave .+ \((\d+)\)\]$", first_line)
device_id, master_id = match_.groups()
os.system(f"xinput float {device_id}")
open("enable_keyboard.sh", "w").write(f"#!/bin/bash\n\nxinput reattach {device_id} {master_id}")
os.chmod("enable_keyboard.sh", 0o700)
