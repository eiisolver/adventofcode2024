import functools
from typing import NamedTuple


class Op(NamedTuple):
    op: str
    args: list[str]
    result: str


file_name = "24_input.txt"
lines = open(file_name, "r").read().splitlines()
empty_line = lines.index("")
wire_values: dict[str, int] = {k: int(v) for k, v in [line.split(": ") for line in lines[:empty_line]]}

swapped_wires = {}

# Pairs of swapped wires (manually detected)
for a0, a1 in [("z13", "vcv"), ("mps", "z25"), ("cqm", "vjv"), ("z19", "vwp")]:
    swapped_wires[a0] = a1
    swapped_wires[a1] = a0


def c(s: str) -> str:
    return swapped_wires.get(s, s)


operations: dict[str, Op] = {}
for arg0, op, arg1, _, result in [line.split(" ") for line in lines[empty_line + 1 :]]:
    operations[c(result)] = Op(op, [arg0, arg1], c(result))
    wire_values[result] = None
    for arg in [arg0, arg1]:
        if arg not in wire_values:
            wire_values[arg] = None

name_map = dict()


def name(wire):
    return name_map.get(wire, wire)


# Rename wires to canonical names based on their operation.
# Output for one typical z will look like:
# ------------ z38 ------------
# Evaluating x37 AND y37 -> AND_37 / x37,y37->vkr
# Evaluating ORR_36 AND XOR_37 -> TMP_37 / bbk,phd->hdb
# Evaluating AND_37 OR TMP_37 -> ORR_37 / vkr,hdb->btj
# Evaluating x38 XOR y38 -> XOR_38 / x38,y38->jwt
# Evaluating ORR_37 XOR XOR_38 -> z38 / btj,jwt->z38
for i in range(100):
    for op in operations.values():
        args = sorted([name(x) for x in op.args])
        a0 = args[0]
        a1 = args[1]
        if args[0][0] == "x" and args[1][0] == "y" and args[0][1:] == args[1][1:]:
            name_map[op.result] = f"{op.op}_{args[1][1:]}"
        elif a0.startswith("ORR_") and a1.startswith("XOR_") and op.op == "AND":
            v0 = int(a0[4:])
            v1 = int(a1[4:])
            if v1 == v0 + 1:
                name_map[op.result] = f"TMP_{a1[4:]}"
        elif a0.startswith("AND_") and op.op == "OR":
            op2 = operations[op.args[1]]
            name_map[op.result] = f"ORR_{a0[4:]}"


@functools.cache
def evaluate_wire(wire: str) -> int:
    if wire in wire_values:
        if wire_values[wire] is not None:
            return wire_values[wire]
    op = operations[wire]
    a0 = op.args[0]
    a1 = op.args[1]
    if name(a0) > name(a1):
        a0, a1 = a1, a0
    args = [evaluate_wire(arg) for arg in [a0, a1]]
    print(f"Evaluating {name(a0)} {op.op} {name(a1)} -> {name(op.result)} / {a0},{a1}->{op.result}")
    if op.op == "AND":
        result = args[0] & args[1]
    elif op.op == "OR":
        result = args[0] | args[1]
    elif op.op == "XOR":
        result = args[0] ^ args[1]
    assert result is not None
    return result


def part1():
    part1 = sum(evaluate_wire(k) << int(k[1:]) for k in wire_values if k[0] == "z")
    print("Part 1:", part1)


# Result was obtained by manually analyzing the output and detecting switched wires.
for i in range(45):
    wire = f"z{i:02}"
    print("------------", wire, "------------")
    evaluate_wire(wire)

print("---- calculating part 1 ----")
part1()
print("Part 2:", ",".join(sorted(swapped_wires.values())))
