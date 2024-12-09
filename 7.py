import re
from typing import List


def evaluate(operands: List[int], bit_mask: int) -> int:
    result = operands[0]
    for index, operand in enumerate(operands[1:]):
        if (bit_mask >> index) & 1 == 0:
            result += operand
        else:
            result *= operand
    return result


def calibrate(target: int, operands: List[int], curr_value: int) -> bool:
    if not operands:
        return target == curr_value
    if curr_value > target:
        return False
    if calibrate(target, operands[1:], curr_value + operands[0]):
        return True
    if calibrate(target, operands[1:], curr_value * operands[0]):
        return True
    return calibrate(target, operands[1:], int(str(curr_value) + str(operands[0])))


lines = open("7_input.txt", "r").read().splitlines()

part1 = 0
part2 = 0
for line in lines:
    nrs = [int(x) for x in re.findall("\d+", line)]
    value = nrs[0]
    operands = nrs[1:]
    for bit_mask in range(2 ** (len(operands) - 1)):
        if evaluate(operands, bit_mask) == value:
            part1 += value
            break
    # Part 2
    if calibrate(value, operands, 0):
        part2 += value
print("Part 1:", part1)
print("Part 2:", part2)
