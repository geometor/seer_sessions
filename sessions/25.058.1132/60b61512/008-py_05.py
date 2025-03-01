"""
Identifies connected groups of yellow pixels and fills the "center" pixels of 3x3 yellow squares with orange.
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

def find_3x3_centers(grid, cluster):
    """
    Finds the center pixels of 3x3 squares of yellow within a cluster.
    Returns a list of (r, c) tuples representing the center coordinates.
    """
    rows, cols = grid.shape
    centers = []
    for r, c in cluster:
        # Check if a 3x3 square centered at (r, c) exists and is all yellow
        is_3x3 = True
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 4):
                    is_3x3 = False
                    break  # Exit inner loops if any part of 3x3 is not yellow or out of bounds
            if not is_3x3:
                break  # Exit outer loop if inner loops found a problem
        if is_3x3:
            centers.append((r, c))
    return centers


def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Identify Yellow Clusters
    yellow_clusters = get_yellow_clusters(input_grid)

    # 2. & 3. Locate 3x3 Centers and Change Color
    for cluster in yellow_clusters:
      centers = find_3x3_centers(input_grid, cluster)
      for r, c in centers:
        output_grid[r,c] = 7

    return output_grid.tolist()