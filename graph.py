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
