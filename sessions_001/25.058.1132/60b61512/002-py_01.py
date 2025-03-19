"""
1. **Identify Yellow Clusters:** Locate all contiguous clusters of yellow (4) pixels in the input grid.  A cluster is defined as one or more yellow pixels that are directly adjacent to each other (horizontally or vertically, not diagonally).

2. **Inner vs. Outer:** Within each yellow cluster, determine "inner" and "outer" yellow pixels. An "outer" yellow pixel is one that is adjacent to at least one white (0) pixel. An "inner" yellow pixel is one that is *only* adjacent to other yellow pixels. If the element has 1 dimension of only 1 cell then all the pixels in this cluster should be considered outer.

3. **Conditional Color Change:** For each yellow cluster within an input, if an "inner" yellow pixel is detected then transform this "inner" pixel into orange (7). Do not change any outer pixels to orange.

4. **Output:** Create the output grid by applying the color changes to the original input grid.
"""

import numpy as np

def _get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell (up, down, left, right)."""
    height, width = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row < height - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < width - 1:
        neighbors.append((row, col + 1))
    return neighbors

def _is_inner(grid, row, col, cluster):
    """Checks if a pixel is an inner pixel within a cluster."""
    if (row,col) not in cluster:
        return False
    
    neighbors = _get_neighbors(grid, row, col)
    for r, c in neighbors:
        if grid[r, c] != 4:
            return False  # Adjacent to a non-yellow pixel
        if (r,c) not in cluster:
            return False
    return True

def _find_clusters(grid, color):
    """Finds all clusters of a given color."""
    clusters = []
    visited = set()
    height, width = grid.shape

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and (r, c) not in visited:
                cluster = set()
                queue = [(r, c)]
                visited.add((r, c))

                while queue:
                    curr_row, curr_col = queue.pop(0)
                    cluster.add((curr_row, curr_col))
                    neighbors = _get_neighbors(grid, curr_row, curr_col)
                    for nr, nc in neighbors:
                        if grid[nr, nc] == color and (nr, nc) not in visited:
                            queue.append((nr, nc))
                            visited.add((nr, nc))
                
                clusters.append(cluster)

    return clusters


def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    output_grid = np.copy(grid)  # Create a copy to modify
    yellow_clusters = _find_clusters(grid, 4)

    for cluster in yellow_clusters:
      for r,c in cluster:
        if _is_inner(grid,r,c, cluster):
            output_grid[r,c] = 7

    return output_grid.tolist()