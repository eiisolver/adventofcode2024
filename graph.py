import heapq


def flood_fill(start: set, neighbour_fn) -> dict:
    """
    Performs flood fill from the given set of start positions.
    neighbour_fn is a callable that takes a node as input,
    and returns the neighbours of that node.
    """
    distances = {node: 0 for node in start}
    added = start
    dist = 0
    while added:
        dist += 1
        new_added = set()
        for node in added:
            for n2 in neighbour_fn(node):
                if n2 not in distances:
                    new_added.add(n2)
                    distances[n2] = dist
        added = new_added
    return distances


def get_floodfill_path(end, distances: dict, neighbour_fn) -> list:
    """
    Returns a path from the start to the given end node, given distances
    obtained from a flood fill calculation (graph must be bidirectional).
    """
    path = [end]
    node = end
    dist = distances[end]
    while dist > 0:
        prev_dist = dist
        for nb in neighbour_fn(node):
            dist2 = distances.get(nb, None)
            if dist2 is not None and dist2 == dist - 1:
                path.append(nb)
                node = nb
                dist -= 1
                break
        if prev_dist == dist:
            raise ValueError(f"No path found, current node: {node}, dist: {dist}")
    path = path[::-1]
    return path


def dijkstra(start, neighbour_fn) -> dict:
    queue = [(0, start)]
    distances = dict()
    distances[start] = 0
    inf = float("inf")
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_distance >= distances.get(current_node, inf):
            continue
        for neighbor, weight in neighbour_fn(current_node):
            distance = current_distance + weight
            if distance < distances.get(neighbor, inf):
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
    return distances
