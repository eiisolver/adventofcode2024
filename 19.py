import functools


lines = open("19_input.txt", "r").read().splitlines()

patterns = lines[0].split(", ")
designs = lines[2:]


@functools.cache
def nr_designs(design: str) -> int:
    if not design:
        return 1
    return sum(nr_designs(design[len(p) :]) for p in patterns if design.startswith(p))


results = [nr_designs(design) for design in designs]
print("Part 1: ", sum(r > 0 for r in results))
print("Part 2: ", sum(results))
