# 1e0a9b12 • 014 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Non-Zero Clusters:** Find all clusters of adjacent, non-zero pixels. A cluster is defined as one or more non-zero pixels that are directly adjacent (not diagonally) to each other in the input grid.
2. **Shift Down:** Move clusters of adjacent, non-zero, pixels down in the grid, 1 row at time.
3. **Consolidate:** Merge moved pixels to the end of the non-zero, adjacent pixels.
4. **Fill with Zeroes**: All other pixels in the grid are zero (white).
"""

import numpy as np

def get_neighbors(grid, r, c):
    neighbors = []
    rows, cols = grid.shape
    if r > 0 and grid[r-1, c] != 0:
        neighbors.append((r - 1, c))
    if r < rows - 1 and grid[r+1, c] != 0:
        neighbors.append((r + 1, c))
    if c > 0 and grid[r, c-1] != 0:
        neighbors.append((r, c - 1))
    if c < cols - 1 and grid[r, c+1] != 0:
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
                    cluster.append((curr_r, curr_c, grid[curr_r, curr_c]))
                    for nr, nc in get_neighbors(grid, curr_r, curr_c):
                        if (nr, nc) not in visited:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
                clusters.append(cluster)
    return clusters

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # Find clusters in the input grid
    clusters = find_clusters(input_grid)

    # Shift and consolidate clusters
    for cluster in clusters:
            #sort by row, makes it easier
            cluster.sort(key=lambda x: x[0])

            for r, c, val in cluster:
                #find rows where it can be moved
                new_r = r
                while new_r < input_grid.shape[0] -1 and output_grid[new_r + 1,c] == 0 and (input_grid[new_r+1,c] == 0 or (new_r+1,c) in [(cr,cc) for cr,cc,_ in cluster]):
                    new_r += 1

                output_grid[new_r,c] = val

    return output_grid
```
