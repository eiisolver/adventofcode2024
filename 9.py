from typing import List, Optional, Tuple


def find_free_space(disk: List[int], start: int, len: int) -> Optional[int]:
    """
    Try to find len free blocks to move the file with given start/length, returns index of first free block
    """
    index = 0
    while index < start:
        if disk[index] is None:
            index2 = index
            while index2 < start and index2 - index < len and disk[index2] is None:
                index2 += 1
            if index2 - index >= len:
                return index
            else:
                index = index2
        else:
            index += 1
    return None


dense_map = open("9_input.txt", "r").read()
disk_map: List[int] = []
# List of (start, length) of contiguous used blocks, used in part 2
used_space: List[Tuple[int, int]] = []

for index, c in enumerate(dense_map):
    n = int(c)
    if index % 2 == 0:
        # Used file blocks
        id = index // 2
        used_space.append((len(disk_map), n))
        disk_map.extend(n * [id])
    else:
        # Unused blocks
        disk_map.extend(n * [None])
disk1 = disk_map[:]
first_free = 0  # index of first free block
last_used = len(disk_map) - 1  # index of last used block
while True:
    # Try to move a used block to a free location
    while last_used > first_free and disk1[last_used] is None:
        last_used -= 1
    while first_free < last_used and disk1[first_free] is not None:
        first_free += 1
    if first_free < last_used:
        disk1[first_free] = disk1[last_used]
        disk1[last_used] = None
    else:
        break
checksum = sum(index * id for index, id in enumerate(disk1) if id is not None)
print("Part 1:", checksum)

disk2 = disk_map[:]
while used_space:
    used_start, used_len = used_space.pop()
    free_start = find_free_space(disk2, used_start, used_len)
    if free_start is not None:
        # The file can be moved
        for i in range(used_len):
            assert disk2[free_start + i] is None
            assert disk2[used_start + i] is not None
            disk2[free_start + i] = disk2[used_start + i]
            disk2[used_start + i] = None

checksum = sum(index * id for index, id in enumerate(disk2) if id is not None)
print("Part 2:", checksum)
