emojis = {}

EMPTY_EMOJI = ":popgoes2:"


for combination, emoji in (
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

    ((False, False, False, False), Exception("Walls with no neighbors are missing in the Phi emoji pack!"))
):
    if combination in emojis:
        raise Exception(f"The {combination} combination is mapped already!")
    emojis[combination] = emoji
if len(emojis) != 16:
    raise Exception("Please, provide all 16 possible combinations.")


print("Would you like your emoji maze to be [compact] or [spacious]?")
maze_type = input("Type in the [maze type] here: ")
if maze_type not in ("compact", "spacious"):
    print(f"Error: the maze type you provided (\"{maze_type}\") is not \"compact\" or \"spacious\".")
    exit(1)
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
            )]
            if isinstance(emoji, Exception):
                raise emoji
        else:
            emoji = EMPTY_EMOJI
        emojis_maze[y][x] = emoji


if maze_type == "compact":
    for row in emojis_maze[::2]:
        print("".join(row[::2]))
elif maze_type == "spacious":
    for row in emojis_maze:
        print("".join(row))
