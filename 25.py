lines = open("25_input.txt", "r").read().splitlines()

locks = []
keys = []

for i in range(0, len(lines), 8):
    if lines[i][0] == "#":
        lock = [0,0,0,0,0]
        for c in range(5):
            for r in range(7):
                if lines[i+r+1][c] == ".":
                    lock[c] = r
                    break
        locks.append(lock)
    else:
        lock = [0,0,0,0,0]
        for c in range(5):
            for r in range(7):
                if lines[i+5-r][c] == ".":
                    lock[c] = r
                    break
        keys.append(lock)

part1 = 0
for key in keys:
    for lock in locks:
        tot = [key[i] + lock[i] for i in range(5)]
        if max(tot) <= 5:
            part1 += 1

print("Part 1:", part1)
