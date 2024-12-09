def is_safe(levels):
    diffs = [lev[0] - lev[1] for lev in zip(levels, levels[1:])]
    safe = all(diff <= 0 for diff in diffs) or all(diff >= 0 for diff in diffs)
    safe = safe and all(abs(diff) in (1, 2, 3) for diff in diffs)
    return safe


reports = [line.split() for line in open("2_input.txt", "r").read().splitlines()]
nr_safe = 0
nr_safe_after_dampen = 0
for report in reports:
    levels = [int(v) for v in report]
    if is_safe(levels):
        nr_safe += 1
    else:
        for i in range(len(levels)):
            levels2 = levels[:]
            del levels2[i]
            if is_safe(levels2):
                nr_safe_after_dampen += 1
                break
print("Part 1:", nr_safe)
print("Part 2:", nr_safe + nr_safe_after_dampen)
