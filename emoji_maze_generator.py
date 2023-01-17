import random

emojis = {}

EMPTY_EMOJI = ":popgoes2:"


def raiser(exc):
    raise exc


def end(direction):
    return lambda: ":phi" + direction + random.choice(("Head", "Nub", "Tail", "Blob")) + ":"


for combination, emoji in (
    # top, bottom, left, right
    ((True, True, True, True), lambda: ":phiCross:"),

    ((False, True, True, True), lambda: ":phiTopSplit:"),
    ((True, False, True, True), lambda: ":phiBottomSplit:"),
    ((True, True, False, True), lambda: ":phiLeftSplit:"),
    ((True, True, True, False), lambda: ":phiRightSplit:"),

    ((False, False, True, True), lambda: ":phiHori:"),
    ((True, True, False, False), lambda: ":phiVerti:"),

    ((False, True, False, True), lambda: ":phiTopLeft:"),
    ((True, False, False, True), lambda: ":phiBottomLeft:"),
    ((False, True, True, False), lambda: ":phiTopRight:"),
    ((True, False, True, False), lambda: ":phiBottomRight:"),

    ((True, False, False, False), end("Bottom")),
    ((False, True, False, False), end("Top")),
    ((False, False, True, False), end("Right")),
    ((False, False, False, True), end("Left")),

    ((False, False, False, False), lambda: raiser(Exception("Walls with no neighbors are missing in the Phi emoji pack!")))
):
    if combination in emojis:
        raise Exception(f"The {combination} combination is mapped already!")
    emojis[combination] = emoji
if len(emojis) != 16:
    raise Exception("Please, provide all 16 possible combinations.")


print("Would you like your emoji maze to be [compact] or [spacious]?")
maze_type = input("Type in the [maze type] here: ")
if maze_type not in ("compact", "spacious"):
    raise Exception(f"Error: the maze type you provided (\"{maze_type}\") is not \"compact\" or \"spacious\".")
print("Type in the maze. Every number sign (#) represents a wall, every space ( ) represents a pathway. End with an empty line.")
lines = []
while True:
    s = input()
    if s == "":
        break
    lines.append(s)
emojis_maze = [[None for _cell in row] for row in lines]


def is_a_wall(x, y):
    try:
        if x < 0 or y < 0:
            raise IndexError
        return lines[y][x] == "#"
    except IndexError:
        return False


for y in range(len(lines)):
    row = lines[y]
    for x in range(len(row)):
        if is_a_wall(x, y):
            emoji = emojis[(
                is_a_wall(x, y - 1),
                is_a_wall(x, y + 1),
                is_a_wall(x - 1, y),
                is_a_wall(x + 1, y)
            )]()
        else:
            emoji = EMPTY_EMOJI
        emojis_maze[y][x] = emoji


if maze_type == "compact":
    for row in emojis_maze[::2]:
        print("".join(row[::2]))
elif maze_type == "spacious":
    for row in emojis_maze:
        print("".join(row))
