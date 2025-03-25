```python
"""
Shifts objects horizontally, then vertically, and coalesces adjacent objects of the same color.
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

def shift_cluster_horizontal(grid, cluster):
    """Shifts a cluster one position left or right, if possible, with gravity."""
    new_grid = np.copy(grid)
    color = grid[cluster[0]]

    # Try shifting left
    can_move_left = True
    for row, col in cluster:
        if col == 0 or (grid[row, col - 1] != 0 and (row, col - 1) not in cluster):
            can_move_left = False
            break

    if can_move_left:
        direction = -1
    else:
        # Try shifting right
        can_move_right = True
        for row, col in cluster:
            if col == grid.shape[1] - 1 or (grid[row, col + 1] != 0 and (row, col + 1) not in cluster):
                can_move_right = False
                break
        if can_move_right:
            direction = 1
        else:
            return grid  # No horizontal movement possible

    # clear the original cluster
    for r, c in cluster:
      new_grid[r,c] = 0

    # Determine maximum downward shift after horizontal move
    new_cluster = []
    max_downward_shift = 0

    for row, col in cluster:
      new_col = col + direction
      max_shift = 0

      # move as far down as possible
      for r in range(row + 1, grid.shape[0]):
        if grid[r,new_col] != 0 and (r,new_col) not in cluster:
          break
        else:
          max_shift += 1
      max_downward_shift = max(max_downward_shift, max_shift)

    # Apply horizontal and vertical shift, combine into new_cluster
    for row, col in cluster:
      new_cluster.append( (row + max_downward_shift, col + direction) )

    # apply the color to the new cluster
    for r, c in new_cluster:
      new_grid[r,c] = color

    return new_grid

def coalesce_clusters(grid):
    """Combines adjacent clusters of the same color, iteratively."""
    new_grid = np.copy(grid)
    
    while True:
        clusters = find_clusters(new_grid)
        coalesced = False
        
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                if i >= len(clusters) or j >= len(clusters): # handle changes to clusters
                    break
                cluster1 = clusters[i]
                cluster2 = clusters[j]

                if cluster1 and cluster2:
                    color1 = new_grid[cluster1[0]]
                    color2 = new_grid[cluster2[0]]

                    if color1 == color2:
                        adjacent = False
                        for row1, col1 in cluster1:
                            for row2, col2 in cluster2:
                                if abs(row1 - row2) <= 1 and abs(col1 - col2) <= 1:
                                    adjacent = True
                                    break
                            if adjacent:
                                break

                        if adjacent:
                            # Combine clusters:  clear cluster2, add to first
                            for row, col in cluster2:
                                new_grid[row, col] = 0
                            for row, col in cluster2:
                                cluster1.append((row,col))
                            clusters[j] = [] # remove
                            coalesced = True
                            # put all cluster1 pixels into the grid with color1
                            for row, col in cluster1:
                                new_grid[row,col] = color1

        if not coalesced:  # Exit when no more coalescing occurs
            break

    return new_grid

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    output_grid = np.copy(input_grid)

    # Horizontal Shifting (with integrated vertical drop)
    for col in range(output_grid.shape[1] - 1, -1, -1):
        clusters_in_col = []
        for row in range(output_grid.shape[0]):
            if output_grid[row, col] != 0:
                for cluster in find_clusters(output_grid):
                    if (row, col) in cluster:
                        clusters_in_col.append(cluster)
        
        # shift
        for cluster in clusters_in_col:
            output_grid = shift_cluster_horizontal(output_grid, cluster)
            
    # Coalescing
    output_grid = coalesce_clusters(output_grid)

    return output_grid
```