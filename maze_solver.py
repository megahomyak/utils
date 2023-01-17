print("Type in the maze. Every number sign (#) represents a wall, every space ( ) represents a pathway. End with an empty line. Represent a starting position with S and an ending position with E.")
lines = []
start = None
end = None
line_index = 0
regular_line_length = None
while True:
    s = input()
    if s == "":
        break
    if regular_line_length is None:
        regular_line_length = len(s)
    elif regular_line_length != len(s):
        raise Exception(f"Line {line_index + 1} has irregular length!")
    try:
        start = (s.index("S"), line_index)
    except ValueError:
        pass
    try:
        end = (s.index("E"), line_index)
    except ValueError:
        pass
    lines.append(list(s))
    line_index += 1
if regular_line_length is None:
    raise Exception("Empty mazes are not accepted!")
if start is None:
    raise Exception("Starting position was not found!")
if end is None:
    raise Exception("Ending position was not found!")


visited = set()
left = [(start, ())]
while len(left) > 0:
    (x, y), previous = left.pop()
    visited.add((x, y))
    for neighbor in ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)):
        neighbor_x, neighbor_y = neighbor
        if (neighbor_x, neighbor_y) == end:
            path = ((neighbor_x, neighbor_y), (x, y)) + previous
            for x, y in path:
                lines[y][x] = "."
            for row in lines:
                print("".join("".join(line) for line in row))
            exit()
        if (
            neighbor_x >= 0
            and neighbor_y >= 0
            and neighbor not in visited
            and neighbor_x < regular_line_length
            and neighbor_y < len(lines)
            and lines[neighbor_y][neighbor_x] == " "
        ):
            left.append((neighbor, previous + ((x, y),)))
else:
    raise Exception("The end is not accessible from the start!")
