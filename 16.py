from collections import defaultdict
from grid import Grid, NESW, Pos
from typing import NamedTuple, Tuple
import heapq

INF = 1e15
lines = open("16_input.txt", "r").read().splitlines()
grid = Grid.create(lines)
start_pos = [pos for pos in grid.positions() if pos.at(lines) == "S"][0]
end_pos = [pos for pos in grid.positions() if pos.at(lines) == "E"][0]


class Node(NamedTuple):
    dir: int  # currently facing direction
    pos: Pos


def opposite_dir(dir: int) -> int:
    return (dir + 2) % 4


def neighbours(graph, n: Node) -> list[Tuple[Node, int]]:
    """
    Returns neighbours, tuples of (node, cost).
    """
    if n in graph:
        return graph[n]
    result = []
    for dir in range(4):
        pos = n.pos + NESW.DIRS[dir]
        if pos.at(lines) != "#" and opposite_dir(dir) != n.dir:
            cost = 1 if dir == n.dir else 1001
            result.append((Node(dir, pos), cost))
    graph[n] = result
    return result


def dijkstra(graph, start: Node) -> dict[Node, int]:
    queue = [(0, start)]
    distances = dict()
    distances[start] = 0
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_distance > distances.get(current_node, INF):
            continue
        for neighbor, weight in neighbours(graph, current_node):
            distance = current_distance + weight
            if distance < distances.get(neighbor, INF):
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
    return distances


graph: dict[Node, list[Tuple[Node, int]]] = dict()
distances = dijkstra(graph, Node(1, start_pos))
best_score = min(distances.get(Node(d, end_pos), INF) for d in range(4))
print("Part 1:", best_score)

reverse_neighbours: dict[Node, set[Node]] = defaultdict(set)
for n, nb in graph.items():
    for n2, _ in nb:
        reverse_neighbours[n2].add(n)

# All nodes that are on any best path to the end.
nodes_on_best_paths: set[Node] = set()

# There could be multiple optimal ways to reach the end node
for d in range(4):
    end = Node(d, end_pos)
    cost = distances.get(end)
    if cost == best_score:
        nodes_on_best_paths.add(end)

# BFS backward from end to start along best paths.
while True:
    added: set[Node] = set()
    for n in nodes_on_best_paths:
        for nb in reverse_neighbours[n]:
            if nb in nodes_on_best_paths:
                continue
            for nb2, cost in graph[nb]:
                if nb2 == n:
                    cost_to_n = cost
            cost_via_nb = distances[nb] + cost_to_n
            if cost_via_nb == distances[n]:
                added.add(nb)
    nodes_on_best_paths |= added
    if not added:
        break
print("Part 2:", len(set(n.pos for n in nodes_on_best_paths)))
