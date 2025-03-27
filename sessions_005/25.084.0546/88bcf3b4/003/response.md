```python
"""
1.  **Identify Objects:** Find all contiguous clusters of non-zero pixels. Each cluster is an object, and pixels of the same color within an object are considered parts of it.

2.  **Iterate through Columns:** Examine the grid column by column, starting from the rightmost column and moving towards the left.

3.  **Determine Shift Potential:** Within each column, determine the objects that are eligible for shifting.
    *   Objects are shifted if they are not in the leftmost column.
    *   The direction of the shift (left or right) depends on where it is blocked by another object.
    *   Consider the grid edge as a blocking object.

4.  **Shift Objects:** Shift each object to the left or right by one or more columns.
   * if any part of an object would collide with a non-zero pixel of another object, the moving object stops immediately before the collision.

5. **Join and Coalesce Objects**: After an object is moved, if parts of another object of the same color exist that are adjacent, combine them.

6. **Vertical Alignment**: objects shift down to the lowest row of a blocking object

7.  **Preserve Background:**  The background (pixels with value 0) is preserved unless overwritten by a shifted object.
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

def shift_cluster(grid, cluster, direction):
    """Shifts a cluster one position to the left or right, if possible."""
    new_grid = np.copy(grid)
    
    #check if we can move cluster, exit early
    can_move = True
    for row, col in cluster:
        new_col = col + direction
        if new_col < 0 or new_col >= grid.shape[1]:
          can_move = False
          break
        if grid[row, new_col] != 0 and (row, new_col) not in cluster:
            can_move = False
            break
            
    if not can_move: return new_grid, False

    # clear cells
    for row, col in cluster:
        new_grid[row, col] = 0

    # move cluster
    new_cluster = []
    for row, col in cluster:
      new_cluster.append((row, col + direction))
    for row, col in new_cluster:
        new_grid[row, col] = grid[row, col-direction]
    return new_grid, True

def get_lowest_row(grid, cluster):
    """Returns the lowest row index within a cluster."""
    lowest_row = -1
    for row, _ in cluster:
        lowest_row = max(lowest_row, row)
    return lowest_row

def vertically_align_cluster(grid, cluster):
    """
    Vertically aligns a cluster downwards, stopping at the bottom of
      the grid or when it encounters another non-zero pixel.
    """
    new_grid = np.copy(grid)
    max_shift = grid.shape[0]

     # clear cells
    for row, col in cluster:
        new_grid[row, col] = 0

    # Find maximum possible downward shift
    for row, col in cluster:
      for r in range(row + 1, grid.shape[0]):
            if grid[r,col] != 0 and (r,col) not in cluster:
              max_shift = min(max_shift, r - row -1)
              break
            elif r == grid.shape[0] - 1:
                max_shift = min(max_shift, r-row)

    new_cluster = []

    for row, col in cluster:
      new_cluster.append((row + max_shift, col))

    for row, col in new_cluster:
      new_grid[row, col] = grid[row - max_shift, col]
    return new_grid

def coalesce_clusters(grid):
    """Combines adjacent clusters of the same color."""
    new_grid = np.copy(grid)
    clusters = find_clusters(new_grid)  # Find clusters in the current grid

    # Iterate through all pairs of clusters
    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            cluster1 = clusters[i]
            cluster2 = clusters[j]
            
            # Check if clusters have the same color
            if cluster1 and cluster2:  # Make sure clusters haven't been emptied
              color1 = new_grid[cluster1[0]]
              color2 = new_grid[cluster2[0]]
              
              if color1 == color2:
                # Check for adjacency (including diagonals)
                adjacent = False
                for row1, col1 in cluster1:
                    for row2, col2 in cluster2:
                        if abs(row1 - row2) <= 1 and abs(col1 - col2) <= 1:
                            adjacent = True
                            break
                    if adjacent:
                        break
                if adjacent: # combine clusters
                    # clear cluster2
                    for row, col in cluster2:
                        new_grid[row,col] = 0
                    # move pixels in cluster2 to cluster1
                    for row, col in cluster2:
                      new_grid[row, col] = color1  # move into first cluster

                    # rebuild clusters - recursion
                    return coalesce_clusters(new_grid)

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

        if len(clusters_in_col) > 0:
          for cluster in clusters_in_col:
            #try to shift left
            output_grid, did_move = shift_cluster(output_grid, cluster, -1)
            #if it can't move left, try to move right
            if not did_move:
               output_grid, did_move = shift_cluster(output_grid, cluster, 1)

    # align vertically
    clusters = find_clusters(output_grid)
    for cluster in clusters:
        output_grid = vertically_align_cluster(output_grid, cluster)
        
    # coalesce clusters
    output_grid = coalesce_clusters(output_grid)

    return output_grid
```