```python
"""
Iterate through the input grid columns from right to left.  Within each column, identify clusters of contiguous, identical, non-zero pixels. Shift these clusters one position to the left if there are any clusters in the column to its left. Preserve the original background (0-value pixels) unless overwritten by shifted clusters.
"""

import numpy as np

def find_clusters(grid):
    """Finds clusters of contiguous non-zero pixels of the same color."""
    clusters = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, cluster):
        """Depth-first search to find contiguous pixels."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
            or grid[row, col] == 0
        ):
            return
        visited[row, col] = True
        cluster.append((row, col))
        dfs(row + 1, col, color, cluster)
        dfs(row - 1, col, color, cluster)
        dfs(row, col + 1, color, cluster)
        dfs(row, col - 1, color, cluster)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                cluster = []
                dfs(row, col, grid[row, col], cluster)
                if cluster:
                    clusters.append(cluster)
    return clusters

def shift_cluster_left(grid, cluster):
    """Shifts a cluster one position to the left, if possible."""
    new_grid = np.copy(grid)
    
    #check if we can move cluster, exit early
    can_move = True
    for row, col in cluster:
        if col == 0:
            can_move = False
            break

    if not can_move: return new_grid

    # clear cells
    for row, col in cluster:
        new_grid[row, col] = 0

    # move cluster
    for row, col in cluster:
        new_grid[row, col - 1] = grid[row, col]
    return new_grid
    

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    
    output_grid = np.copy(input_grid)
    
    # iterate by columns, right to left
    for col in range(output_grid.shape[1] - 1, -1, -1):
        clusters_in_col = []
        
        # any clusters in the column?
        for row in range(output_grid.shape[0]):
             if output_grid[row, col] != 0:
                 #get the object and try to shift
                 for cluster in find_clusters(output_grid):
                     for r,c in cluster:
                         if r == row and c == col:
                             clusters_in_col.append(cluster)
                             
        # check if there are any other clusters to the left, and
        #   we have clusters to shift
        if col > 0 and len(clusters_in_col) > 0:
            left_cells = output_grid[:, :col]
            if np.any(left_cells != 0):
              for cluster in clusters_in_col:
                output_grid = shift_cluster_left(output_grid, cluster)

    return output_grid
```