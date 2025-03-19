"""
Transforms the input grid by identifying the largest contiguous cluster of non-white pixels,
replacing all but one pixel in the cluster with red (2), keeping the original color of a single pixel,
and clearing all other pixels to white (0).
"""

import numpy as np
from collections import deque

def find_largest_cluster(grid):
    """Finds the largest contiguous cluster of non-white pixels."""
    rows, cols = len(grid), len(grid[0])
    visited = set()
    max_cluster = []

    def get_neighbors(r, c):
        """Gets valid neighbors of a cell."""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbors.append((nr, nc))
        return neighbors

    def bfs(start_r, start_c):
        """Performs Breadth-First Search to find a cluster."""
        queue = deque([(start_r, start_c)])
        visited.add((start_r, start_c))
        cluster = [(start_r, start_c)]
        colors = {}
        colors[grid[start_r][start_c]] = 1

        while queue:
            r, c = queue.popleft()
            for nr, nc in get_neighbors(r, c):
                if (nr, nc) not in visited and grid[nr][nc] != 0:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
                    cluster.append((nr, nc))
                    if grid[nr][nc] not in colors:
                        colors[grid[nr][nc]] = 0
                    colors[grid[nr][nc]]+=1
        return cluster, colors

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                cluster, colors = bfs(r, c)
                if len(cluster) > len(max_cluster):
                    max_cluster = cluster
                    max_colors = colors

    return max_cluster, max_colors

def select_center_pixel(grid, cluster, colors):
    """ selects a single pixel within the cluster to remain to original color """

    # if only one color exists other than 0(white), then return the first
    if len(colors) == 1:
       return cluster[0]

    # find coordinate of pixel that has max count
    max_count = 0
    max_color = -1

    for color in colors:
        if colors[color] > max_count:
            max_count = colors[color]
            max_color = color

    for (r,c) in cluster:
       if grid[r][c] == max_color:
          return (r,c)

    return cluster[0] # default

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    grid = np.array(input_grid)
    rows, cols = len(grid), len(grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find the largest contiguous cluster
    cluster, colors = find_largest_cluster(grid)

    # if no cluster found, return all white grid
    if not cluster:
       return output_grid

    # select center pixel
    center_pixel = select_center_pixel(grid, cluster, colors)


    # Recolor the cluster to red (2), except center pixel
    for r, c in cluster:
        output_grid[r, c] = 2
    output_grid[center_pixel] = grid[center_pixel]
    return output_grid.tolist()