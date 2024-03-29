import random
from itertools import chain


BEGINNING_MARK = ":HandHello:"
END_MARK = ":HandClap:"
ARROW_LEFT = ":HandPointLeft:"
ARROW_RIGHT = ":HandPointRight:"
ARROW_UP = ":HandPointUp:"
ARROW_DOWN = ":HandPointDown:"
EMPTY_SPACE = ":popgoes2:"

MAZE_HEIGHT = 15
MAZE_WIDTH = 15

PATH_LENGTH = 20

BIASES = ((-1, 0, ARROW_LEFT), (1, 0, ARROW_RIGHT), (0, 1, ARROW_DOWN), (0, -1, ARROW_UP))


def out_of_bounds(x, y):
    return x < 0 or y < 0 or y >= MAZE_HEIGHT or x >= MAZE_WIDTH


def get_next_position_variations(origin_x, origin_y, pointed_at):
    next_position_variations = []
    for x_bias, y_bias, arrow in BIASES:
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
                    out_of_bounds(x, y)
                    or (x, y) in pointed_at
                ):
                    break
                fn(x, y)
    return next_position_variations


def get_the_right_path(origin_x, origin_y, arrow, pointed_at, path):
    path = path + [(origin_x, origin_y, arrow)]
    if len(path) == PATH_LENGTH:
        return path
    variations = get_next_position_variations(origin_x, origin_y, pointed_at)
    random.shuffle(variations)
    for x, y, arrow, pointed_at in variations:
        right_path = get_the_right_path(x, y, arrow, pointed_at, path)
        if right_path is not None:
            return right_path


def print_the_maze():
    print(BEGINNING_MARK)
    print("\n".join("".join(row) for row in maze))


path = get_the_right_path(0, 0, None, {(0, 0)}, [])
occupied = set()
if path is None:
    raise Exception(f"The grid is not big enough to contain a path of length {PATH_LENGTH}!")
maze = [[EMPTY_SPACE for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
for (x, y), arrow in zip(
    map(lambda cell: (cell[0], cell[1]), path),
    chain(
        map(lambda cell: cell[2], path[1:]),
        iter((END_MARK,))
    )
):
    occupied.add((x, y))
    maze[y][x] = arrow
print("Solution:")
print_the_maze()
for cell_y in range(MAZE_HEIGHT):
    for cell_x in range(MAZE_WIDTH):
        if (cell_x, cell_y) not in occupied:
            biases = list(BIASES)
            random.shuffle(biases)
            for x_bias, y_bias, arrow in biases:
                x = cell_x
                y = cell_y
                while not out_of_bounds(x, y):
                    x += x_bias
                    y += y_bias
                    if (x, y) in occupied:
                        break
                else:
                    break
            else:
                arrow = EMPTY_SPACE
            maze[cell_y][cell_x] = arrow
print(f"\nRules: start from the cell immediately below the starting cell ({BEGINNING_MARK}), end at the ending cell ({END_MARK}). You can go in the direction of an arrow as many cells as you want. If you have nowhere to go or you landed on an empty spot ({EMPTY_SPACE}), the game is over.")
print_the_maze()
