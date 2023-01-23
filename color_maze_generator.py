MIN_PATH_LENGTH = 30
MARKS = [":PhiStop:", ":PhiTrue:", ":PhiFury:", ":PhiWat:"]
BEGINNING_MARK = "::"
END_MARK = ""
MAZE_HEIGHT = 10
MAZE_WIDTH = 10


def 


def get_next_position_variations(origin_x, origin_y, marks):
    for x_bias, y_bias in ((-1, 0), (1, 0), (0, 1), (0, -1)):
        x = origin_x + x_bias
        y = origin_y + y_bias
        if (x, y) not in marks:
            mark = MARKS[marks % len(MARKS)]
            yield (x, y, mark, marks | {(x, y)})


def get_mark(distance):
    return MARKS[distance % len(MARKS)]


def get_cell(cells, x, y):
    if x < 0 or y < 0:
        raise IndexError
    return cells[y][x]


def make_a_maze(cells, current, distance, last_bias):
    x, y = current
    for x_bias, y_bias in ((-1, 0), (1, 0), (0, 1), (0, -1)):
        if (-x_bias, -y_bias) == last_bias:
            continue
        try:
            cell = get_cell(cells, x + x_bias, y + y_bias)
        except IndexError:
            continue
        if get_mark(distance + 1) == cell:


def get_the_right_path(x, y, distance, cells):
    cells = cells.copy()
    for x_bias, y_bias in ((-1, 0), (1, 0), (0, 1), (0, -1)):
        x = origin_x + x_bias
        y = origin_y + y_bias
