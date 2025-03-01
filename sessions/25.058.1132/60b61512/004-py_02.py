"""
Detects connected groups of yellow pixels and fills the "inner" pixels with orange.
Inner is defined as having horizontal and vertical yellow neighbors.
"""

import numpy as np

def get_yellow_clusters(grid):
    """Finds all contiguous blocks of yellow (4) pixels."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    clusters = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_cluster):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != 4:
            return
        visited[r, c] = True
        current_cluster.append((r, c))
        # Check all 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(r + dr, c + dc, current_cluster)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 4 and not visited[r, c]:
                current_cluster = []
                dfs(r, c, current_cluster)
                clusters.append(current_cluster)
    return clusters

def is_interior(grid, r, c):
    """Checks if a yellow pixel is "interior" based on neighbors."""
    rows, cols = grid.shape

    # Check for yellow neighbors above, below, left, and right.
    above = (r > 0 and grid[r-1, c] == 4)
    below = (r < rows - 1 and grid[r+1, c] == 4)
    left  = (c > 0 and grid[r, c-1] == 4)
    right = (c < cols - 1 and grid[r, c+1] == 4)

    return (above and below) or (left and right)


def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Identify Yellow Clusters
    yellow_clusters = get_yellow_clusters(input_grid)

    # 2. & 3. Locate Interior Yellow Pixels and Change Color
    for cluster in yellow_clusters:
        for r, c in cluster:
            if is_interior(input_grid, r, c):
                output_grid[r, c] = 7

    return output_grid.tolist()