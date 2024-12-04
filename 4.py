def count_xmas(lines, i, j):
    count = 0
    for d in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
        for k in range(4):
            x, y = i + k*d[0], j + k*d[1]
            if x < 0 or x >= len(lines[0]) or y < 0 or y >= len(lines):
                break
            if lines[y][x] != "XMAS"[k]:
                break
            if k == 3:
                count += 1
    return count

def count_cross(lines, row, col):
    a = lines[row-1][col-1] + lines[row][col] + lines[row+1][col+1]
    if a != "SAM" and a != "MAS":
        return 0
    b = lines[row-1][col+1] + lines[row][col] + lines[row+1][col-1]
    return 1 if b == "SAM" or b == "MAS" else 0

lines = open("4_input.txt", "r").read().splitlines()
count = 0
for row in range(len(lines)):
    for col in range(len(lines[0])):
        count += count_xmas(lines, col, row)
print("Part 1:", count)
count = 0
for row in range(1, len(lines)-1):
    for col in range(1, len(lines[0])-1):
        count += count_cross(lines, col, row)
print("Part 2:", count)