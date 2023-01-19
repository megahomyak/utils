import random


BEGINNING_MARK = "B"
END_MARK = "E"
ARROW_LEFT = "<"
ARROW_RIGHT = ">"
ARROW_UP = "^"
ARROW_DOWN = "V"

MAZE_HEIGHT = 10
MAZE_WIDTH = 10

PATH_LENGTH = 10


def get_next_position_variations(origin_x, origin_y, pointed_at):
    next_position_variations = []
    for x_bias, y_bias, arrow in ((-1, 0, ARROW_LEFT), (1, 0, ARROW_RIGHT), (0, 1, ARROW_DOWN), (0, -1, ARROW_UP)):
        new_pointed_at = set()
        for fn in (
            lambda x, y: new_pointed_at.add((x, y)),
            lambda x, y: next_position_variations.append(
                (x, y, arrow, pointed_at | new_pointed_at | {(origin_x, origin_y)})
            )
        ):
            x = origin_x
            y = origin_y
            while True:
                x += x_bias
                y += y_bias
                if (
                    x < 0
                    or y < 0
                    or y >= MAZE_HEIGHT
                    or x >= MAZE_WIDTH
                    or (x, y) in pointed_at
                ):
                    break
                fn(x, y)
    return next_position_variations


def get_the_right_path(origin_x, origin_y, arrow, pointed_at, path):
    path = path + [(origin_x, origin_y, arrow)]
    if len(path) == 10:
        return path
    variations = get_next_position_variations(origin_x, origin_y, pointed_at)
    random.shuffle(variations)
    for x, y, arrow, pointed_at in variations:
        right_path = get_the_right_path(x, y, arrow, pointed_at, path)
        if right_path is not None:
            return right_path


path = get_the_right_path(0, 0, None, {(0, 0)}, [])
if path is None:
    raise Exception("Path of the right length cannot be built!")
maze = [[" " for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
cells = iter(path)
old_x, old_y, old_arrow = next(cells)
for new_x, new_y, new_arrow in path:
    maze[old_y][old_x] = new_arrow
    old_x = new_x
    old_arrow = new_arrow
    old_y = new_y
end_x, end_y, _end_arrow = path[-1]
maze[end_y][end_x] = END_MARK
print(BEGINNING_MARK)
print("\n".join("".join(row) for row in maze))
