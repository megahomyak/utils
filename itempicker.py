import clear_screen
from pynput import keyboard
from pynput.keyboard import Key

index = 0

BIAS_SIZE = 3
WINDOW_SIZE = BIAS_SIZE * 2 + 1

def display():
    clear_screen.clear()
    beginning_index = max(min(index - BIAS_SIZE, len(items) - WINDOW_SIZE), 0)
    end_index = beginning_index + WINDOW_SIZE
    items_view = items[beginning_index:end_index]
    biased_index = index - beginning_index
    for view_index, item in enumerate(items_view):
        if view_index == biased_index:
            print("* " + item)
        else:
            print("  " + item)

items = """a
b
c
d
e
f
g
h
i
j
k
l""".splitlines()


def on_key_press(key):
    global index
    if key == Key.up:
        if index != 0:
            index -= 1
    elif key == Key.down:
        if index != len(items) - 1:
            index += 1
    display()

display()

with keyboard.Listener(on_press=on_key_press) as listener:
    listener.join()
