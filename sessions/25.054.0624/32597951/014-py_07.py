"""
1.  **Identify Azure Clusters:** Locate all clusters of azure (8) pixels within the input grid. A cluster is defined as one or more azure pixels that are contiguously connected (horizontally, vertically, or diagonally).

2.  **Identify inner and outer Blue Pixels:** For each azure cluster locate the blue(1) pixels. For each cluster, blue pixels can be one of two types.
    *   Inner Blue Pixels. Those blue(1) pixels that are adjacent to azure(8) pixels *and* also adjacent to blue(1) pixels that are *not* adjecent to azure(8) pixels
    *   Outer Blue Pixels: those blue(1) pixels that are adjacent to azure(8) pixels *and* are *not* inner blue pixels.

3.  **Conditional Replacement, Outer Blue Pixels:** For all "Outer Blue Pixels", change any that are adjacent to azure(8) pixels to green(3).

4.  **Conditional Replacement, Inner Blue Pixels:** For all "Inner Blue Pixels", change any that are adjacent to azure(8) pixels to green(3).
"""

import numpy as np
from collections import deque

def find_clusters(grid, color):
    """Finds clusters of a specific color in the grid."""
    visited = set()
    clusters = []

    def get_neighbors(r, c):
        """Returns valid neighbors (within bounds and same color)."""
        rows, cols = grid.shape
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == color:
                    neighbors.append((nr, nc))
        return neighbors

    def bfs(start_r, start_c):
        """Performs Breadth-First Search to find a cluster."""
        queue = deque([(start_r, start_c)])
        cluster = set()
        visited.add((start_r, start_c))

        while queue:
            r, c = queue.popleft()
            cluster.add((r, c))
            for nr, nc in get_neighbors(r, c):
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        return cluster

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                clusters.append(bfs(r, c))
    return clusters

def get_adjacent_pixels(grid, cluster, color):
    """get pixels of a specific color adjacent to the cluster"""
    rows, cols = grid.shape
    adjacent_pixels = set()
    
    for r,c in cluster:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r+dr, c+dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr,nc] == color:
                    adjacent_pixels.add((nr,nc))
    return adjacent_pixels


def get_blue_pixel_types(grid, azure_cluster):
    """Classifies blue pixels adjacent to an azure cluster."""
    
    adjacent_blues = get_adjacent_pixels(grid, azure_cluster, 1)
    
    inner_blue_pixels = set()
    outer_blue_pixels = set()

    for b_r, b_c in adjacent_blues:
        is_inner = False
        
        #check neighbors of this blue pixel
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue

                nr, nc = b_r + dr, b_c + dc
                if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                    if grid[nr,nc] == 1 and (nr,nc) not in adjacent_blues:
                        is_inner = True
                        break
            if is_inner: break # optimization
        if is_inner:
            inner_blue_pixels.add((b_r,b_c))
        else:
            outer_blue_pixels.add((b_r,b_c))

    return inner_blue_pixels, outer_blue_pixels

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    output_grid = grid.copy()

    azure_clusters = find_clusters(grid, 8)

    for cluster in azure_clusters:
        inner_blue_pixels, outer_blue_pixels = get_blue_pixel_types(grid, cluster)

        # change outer pixels
        for r, c in outer_blue_pixels:
            output_grid[r, c] = 3
        # change inner pixels
        for r,c in inner_blue_pixels:
            output_grid[r,c] = 3
            

    return output_grid.tolist()  # Convert back to list