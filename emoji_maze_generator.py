emojis = {}

EMPTY_EMOJI = ":popgoes2:"


for combination, emoji in (
    # Must be the all 16 combinations for full coverage (there are 15, though: the all-False one is not included)
    # top, bottom, left, right
    ((True, True, True, True), ":phiCross:"),

    ((False, True, True, True), ":phiTopSplit:"),
    ((True, False, True, True), ":phiBottomSplit:"),
    ((True, True, False, True), ":phiLeftSplit:"),
    ((True, True, True, False), ":phiRightSplit:"),

    ((False, False, True, True), ":phiHori:"),
    ((True, True, False, False), ":phiVerti:"),

    ((False, True, False, True), ":phiTopLeft:"),
    ((True, False, False, True), ":phiBottomLeft:"),
    ((False, True, True, False), ":phiTopRight:"),
    ((True, False, True, False), ":phiBottomRight:"),

    ((True, False, False, False), ":phiBottomNub:"),
    ((False, True, False, False), ":phiTopNub:"),
    ((False, False, True, False), ":phiRightNub:"),
    ((False, False, False, True), ":phiLeftNub:"),
):
    if combination in emojis:
        raise Exception(f"The {combination} combination is mapped already!")
    emojis[combination] = emoji


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
        emojis_maze[y][x] = emojis[(
            is_a_wall(x, y - 1),
            is_a_wall(x, y + 1),
            is_a_wall(x - 1, y),
            is_a_wall(x + 1, y)
        )] if is_a_wall(x, y) else EMPTY_EMOJI


for row in emojis_maze:
    print("".join(row))
