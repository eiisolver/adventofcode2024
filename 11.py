import functools


@functools.cache
def nr_stones_after_blinks(nr: int, blinks: int) -> int:
    if blinks == 0:
        return 1
    if nr == 0:
        return nr_stones_after_blinks(1, blinks - 1)
    nr_str = str(nr)
    if len(nr_str) % 2 == 0:
        half = len(nr_str) // 2
        nr1 = int(nr_str[:half])
        nr2 = int(nr_str[half:])
        return nr_stones_after_blinks(nr1, blinks - 1) + nr_stones_after_blinks(nr2, blinks - 1)
    return nr_stones_after_blinks(2024 * nr, blinks - 1)


def sum_of_stones(numbers: list[int], nr_blinks) -> int:
    return sum(nr_stones_after_blinks(nr, nr_blinks) for nr in numbers)


numbers = [int(nr) for nr in open("11_input.txt", "r").read().split()]
print("Part 1:", sum_of_stones(numbers, 25))
print("Part 2:", sum_of_stones(numbers, 75))
