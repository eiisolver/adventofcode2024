import re
import numpy as np

lines = open("13_input.txt", "r").read().splitlines()
nrs = [[int(x) for x in re.findall("\d+", line)] for line in lines]
result = [0, 0]
DELTA = 10000000000000
for i in range(0, len(lines), 4):
    button_a = nrs[i]
    button_b = nrs[i + 1]
    prize1 = nrs[i + 2]
    prize2 = [t + DELTA for t in prize1]
    prize = [prize1, prize2]
    for part in range(2):
        A = np.array([[button_a[0], button_b[0]], [button_a[1], button_b[1]]])
        P = prize[part]
        solution = np.linalg.solve(A, P)
        a = round(solution[0])
        b = round(solution[1])
        if all(a * button_a[i] + b * button_b[i] == P[i] for i in range(2)):
            result[part] += 3 * a + b


print("Part 1:", result[0])
print("Part 2:", result[1])
