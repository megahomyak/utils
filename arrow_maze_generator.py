from typing import List, Tuple
import random


BEGINNING_MARK = "B"
END_MARK = "E"
ARROW_LEFT = "<"
ARROW_RIGHT = ">"
ARROW_UP = "^"
ARROW_DOWN = "V"

MAZE_HEIGHT = 10
MAZE_WIDTH = 10

MIN_PATH_LENGTH = 10
MAX_PATH_LENGTH = 15


def get_unoccupied(cell: Tuple[int, int, List[Tuple[int, int]]], direction: str):
    x, y, path = cell
    path = set((other_x, other_y) for other_x, other_y in path)
    if direction in ("up", "down"):
        if any((x, i) in path for i in range())
    bias_x, bias_y = bias
    print(path)
    matching = []
    while True:
        x += bias_x
        y += bias_y
        if x < 0 or y < 0 or x >= MAZE_WIDTH or y >= MAZE_HEIGHT:
            break
        if (x, y) in path:
            return []
        matching.append((x, y))
    return matching


left = [(0, 0, [])]
while left:
    cell = left.pop()
    x, y, path = cell
    if len(path) in range(MIN_PATH_LENGTH, MAX_PATH_LENGTH + 1):
        end = cell
        break
    new = []
    for bias_x, bias_y, direction in (
        (-1, 0, ARROW_LEFT),
        (0, -1, ARROW_UP),
        (1, 0, ARROW_RIGHT),
        (0, 1, ARROW_DOWN)
    ):
        try:
            if direction == path[-1][2]:
                continue
        except IndexError:
            pass
        unoccupied = get_unoccupied(cell, (bias_x, bias_y))
        random.shuffle(unoccupied)
        for next_x, next_y in unoccupied:
            new.append((next_x, next_y, path + [(x, y, direction)]))
    left.extend(new)
else:
    raise Exception("Path of a right length cannot be built!")

maze = [[" " for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
end_x, end_y, end_path = end
print(end_path)
maze[end_y][end_x] = END_MARK
for node in end_path:
    x, y, direction = node
    maze[y][x] = direction
print(BEGINNING_MARK)
print("\n".join("".join(row) for row in maze))
