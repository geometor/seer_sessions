# 1e0a9b12 • 018 • refine_coder

---
```python
"""
1. **Identify Initial Clusters:** Find all contiguous clusters of non-zero pixels in the input grid.  These are the "source" clusters.
2. **Process Each Source Cluster:** For each source cluster, determine its movement potential.
3. **Move Down:** A source cluster can move down *only if* every pixel in the cluster has a clear path downwards.  A clear path is defined as:
    - The cell directly below is empty (value 0), OR
    - The cell directly below is occupied by a non-zero pixel that is *not* part of any source cluster (i.e. the pixel was created during a downward move).
4. **Move as a Unit:** If a source cluster can move, move *all* its pixels down by one row.  Crucially, a cluster moves as a single unit.
5. **Repeat:** Continue moving the cluster down one row at a time until it can no longer move (either it hits the bottom, or it encounters a pixel from another *source* cluster).
6. **No Further Movement:** Once a cluster has stopped moving, it cannot move again, even if empty spaces open up below it later.
7. Fill empty spaces.
"""

import numpy as np

def get_neighbors(grid, r, c):
    neighbors = []
    rows, cols = grid.shape
    if r > 0:
        neighbors.append((r - 1, c))
    if r < rows - 1:
        neighbors.append((r + 1, c))
    if c > 0:
        neighbors.append((r, c - 1))
    if c < cols - 1:
        neighbors.append((r, c + 1))
    return neighbors

def find_clusters(grid):
    clusters = []
    visited = set()
    rows, cols = grid.shape

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                cluster = []
                queue = [(r, c)]
                visited.add((r, c))

                while queue:
                    curr_r, curr_c = queue.pop(0)
                    cluster.append((curr_r, curr_c))
                    for nr, nc in get_neighbors(grid, curr_r, curr_c):
                        if (nr, nc) not in visited and grid[nr,nc] != 0:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
                clusters.append(cluster)
    return clusters

def can_move_cluster(grid, cluster):
    rows, _ = grid.shape
    for r, c in cluster:
        if r + 1 >= rows:  # Reached bottom
            return False
        if grid[r+1, c] != 0 and (r + 1, c) not in [(r_temp+1,c_temp) for r_temp,c_temp in cluster]:
          return False #Blocked
    return True

def move_cluster(grid, cluster):
  new_cluster = []
  for r,c in cluster:
    grid[r+1,c] = grid[r,c]
    grid[r,c] = 0
    new_cluster.append((r+1,c))
  return grid, new_cluster

def transform(input_grid):
    # initialize output_grid as a copy to avoid modifying the input directly.
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # Find original clusters
    original_clusters = find_clusters(output_grid)
    moved_clusters = []

    # Iterate through each cluster
    for cluster in original_clusters:
      while can_move_cluster(output_grid, cluster):
          output_grid, cluster = move_cluster(output_grid, cluster)


    return output_grid
```
