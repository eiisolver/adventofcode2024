import re

text = open("3_input.txt", "r").read()
matches = re.findall(r"mul\([\d]{1,3},[\d]{1,3}\)", text)
sum = 0
for m in matches:
    numbers = [int(nr) for nr in re.findall("\d+", m)]
    sum += numbers[0] * numbers[1]
print("Part 1:", sum)

# Part 2
matches = re.findall(r"(mul\([\d]{1,3},[\d]{1,3}\))|(do\(\))|(don't\(\))", text)
sum = 0
enabled = True
for m in matches:
    if m[0] and enabled:
        numbers = [int(nr) for nr in re.findall("\d+", m[0])]
        sum += numbers[0] * numbers[1]
    elif m[1]:
        # do()
        enabled = True
    elif m[2]:
        # don't()
        enabled = False
print("Part 2:", sum)
