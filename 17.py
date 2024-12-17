lines = open("17_input.txt", "r").read().splitlines()

reg = [0, 0, 0]
for i in range(3):
    reg[i] = int(lines[i][12:])

program = [int(v) for v in lines[4][9::2]]


def combo(reg, v) -> int:
    return v if v <= 3 else reg[v - 4]


def reg_str(reg):
    return [oct(v) for v in reg]


INSTR = ["div->a", "xor B ", "stor b", "jnz A ", "xor BC", "out   ", "div->b", "div->c"]
debug = True


def exec(program, reg) -> list[int]:
    if debug:
        print("Exec", program, ", regs", reg_str(reg))
    pc = 0
    output = []
    while pc < len(program):
        op = program[pc]
        operand = program[pc + 1]
        if debug:
            print("OP:", op, INSTR[op], "with", operand, ", regs:", reg_str(reg), ", pc = ", pc, ", out:", output)

        if op == 0:
            # A = A / 2^combo(op)
            reg[0] = reg[0] // (2 ** combo(reg, operand))
        elif op == 1:
            # B = B xor operand
            reg[1] = reg[1] ^ operand
        elif op == 2:
            # B = combo(op)
            reg[1] = combo(reg, operand) % 8
        elif op == 3:
            # jnz
            pc = pc + 2 if reg[0] == 0 else operand
            continue
        elif op == 4:
            # B = xor B C
            reg[1] = reg[1] ^ reg[2]
        elif op == 5:
            # output B
            output.append(combo(reg, operand) % 8)
        elif op == 6:
            # B = A / 2^combo(op)
            reg[1] = reg[0] // (2 ** combo(reg, operand))
        elif op == 7:
            # C = A / 2^combo(op)
            reg[2] = (reg[0] // (2 ** combo(reg, operand))) % 8
        pc += 2
    return output


output = exec(program, reg)
print("Part 1:", ",".join(str(v) for v in output))

debug = False
solutions = [0]
part2 = None
# Attempt to generate the tail of the program.
# Build upon previous results
for i in range(len(program)):
    new_solutions = []
    for solution in solutions:
        for v in range(8):
            reg_a = 8 * solution + v
            output = exec(program, [reg_a, 0, 0])
            if output == program[-i - 1 :]:
                print(oct(reg_a), "->", output, ", dec:", reg_a)
                new_solutions.append(reg_a)
                if part2 is None and program == output:
                    part2 = reg_a
                    print("Yes!")
    solutions = new_solutions

print("Part 2:", part2)
