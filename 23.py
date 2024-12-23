from collections import defaultdict

file_name = "23_input.txt"
connections = [line.split("-") for line in open(file_name, "r").read().splitlines()]
neighbours: dict[set[str]] = defaultdict(set)

for a, b in connections:
    neighbours[a].add(b)
    neighbours[b].add(a)

# Calc all 3-connected components.
components: set[tuple[str]] = set()
part1: set[tuple[str]] = set()
for a, b in connections:
    for c in neighbours[a].intersection(neighbours[b]):
        elem = tuple(sorted([a, b, c]))
        components.add(elem)
        if a[0] == "t" or b[0] == "t" or c[0] == "t":
            part1.add(elem)
print("Part 1:", len(part1))

# Extend components with 1 extra node until there is only one component left.
while len(components) > 1:
    next_components: set[tuple[str]] = set()
    for component in components:
        for n in neighbours[next(iter(component))]:
            connected_to_all = True
            for n2 in component:
                if n2 not in neighbours[n]:
                    connected_to_all = False
                    break
            if connected_to_all:
                next_components.add(tuple(sorted(list(component) + [n])))
    components = next_components

print("Part 2:", ",".join(components.pop()))
