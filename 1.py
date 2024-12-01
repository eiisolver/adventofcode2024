ids = [line.split() for line in open("1_input.txt", "r").read().splitlines()]
list0 = [int(e[0]) for e in ids]
list1 = [int(e[1]) for e in ids]
list0.sort()
list1.sort()
result1 = sum(abs(list0[i] - list1[i]) for i in range(len(list0)))
print(result1)
result2 = sum(a * list1.count(a) for a in list0)
print(result2)
