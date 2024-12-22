from collections import defaultdict


def prune(secret_nr):
    return secret_nr % 16777216


def mix(secret_nr, nr):
    return secret_nr ^ nr


def get_next(nr: int) -> int:
    r = nr * 64
    r = prune(mix(r, nr))
    r = prune(mix(r, r // 32))
    r = prune(mix(r, r * 2048))
    return r


nrs = [int(line) for line in open("22_input.txt", "r").read().splitlines()]

part1 = 0
total_bananas_per_change = defaultdict(int)
for nr in nrs:
    bananas_per_change = dict()
    changes = []
    for i in range(2000):
        new_nr = get_next(nr)
        price = new_nr % 10
        changes.append(price - (nr % 10))
        if len(changes) >= 4:
            change = tuple(changes[-4:])
            if change not in bananas_per_change:
                bananas_per_change[change] = price
        nr = new_nr
    part1 += nr
    for k, v in bananas_per_change.items():
        total_bananas_per_change[k] += v

print("Part 1:", part1)
print("Part 2:", max(total_bananas_per_change.values()))
