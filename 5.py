from collections import defaultdict
from functools import cmp_to_key
import re


lines = open("5_input.txt", "r").read().splitlines()
# Contains for each page the set of pages that may not appear after
forbidden_after = defaultdict(set)


def compare_pages(page1, page2):
    if page1 in forbidden_after[page2]:
        return -1
    if page2 in forbidden_after[page1]:
        return 1
    return 0


part1 = 0
part2 = 0
for line in lines:
    nrs = [int(x) for x in re.findall("\d+", line)]
    if "|" in line:
        forbidden_after[nrs[1]].add(nrs[0])
    elif "," in line:
        sorted_nrs = sorted(nrs, key=cmp_to_key(compare_pages))
        middle = sorted_nrs[len(sorted_nrs) // 2]
        if nrs == sorted_nrs:
            part1 += middle
        else:
            part2 += middle

print("Part 1:", part1)
print("Part 2:", part2)
