# 88a10436 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify:** Locate the contiguous cluster of non-zero pixels in the top-left corner of the input grid ( `cluster_1`). Also identify `pixel_1`, which is equal to color 5.
2.  **Mirror:** Create a vertically mirrored copy of `cluster_1`. The mirror axis is the horizontal line passing through the vertical center of the original object (`cluster_1`).
3.  **Translate:** Move the mirrored cluster to the bottom of the grid. Maintain the original column positions of each pixel within the cluster. In the new grid the mirrored cluster starts in the row that has the same number in the complete grid as the first row below `cluster_1` in the input grid.
4.  **Remove:** Remove pixel of color 5 (`pixel_1`) from the grid.
5. **Output**: Combine all transformed clusters and remaining pixels to generate output grid
"""

import numpy as np

def find_cluster(grid):
    """Finds the top-left contiguous non-zero cluster."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    cluster = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols and grid[r, c] != 0 and not visited[r, c]

    def dfs(r, c):
        if not is_valid(r, c):
            return
        visited[r, c] = True
        cluster.append((r, c, grid[r, c]))
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r,c] != 0:
                dfs(r,c)
                return cluster, visited #return after finding first cluster

    return [], visited #return if no cluster

def find_pixel(grid, color):
    """Finds coordinates of a pixel with the given color."""
    rows, cols = grid.shape
    for r in range(rows):
      for c in range(cols):
        if grid[r,c] == color:
          return [(r,c,color)]
    return []


def mirror_cluster(cluster):
    """Vertically mirrors the cluster."""
    mirrored_cluster = []
    if not cluster:
      return mirrored_cluster
    min_row = min(r for r, _, _ in cluster)
    max_row = max(r for r, _, _ in cluster)
    # mirror_axis = (min_row + max_row) / 2  #not needed

    for r, c, color in cluster:
        # new_r = int(2 * mirror_axis - r)
        new_r = max_row - (r - min_row)  # Simplified mirroring
        mirrored_cluster.append((new_r, c, color))
    return mirrored_cluster


def translate_cluster(cluster, grid):
    """Translates mirrored to the bottom, maintaining column positions."""
    translated_cluster = []
    if not cluster:
        return translated_cluster

    rows, _ = grid.shape
    
    cluster_coords, _ = find_cluster(grid)

    empty_row = 0
    for r in range(rows):
        if all(grid[r,c] == 0 for _,c,_ in cluster_coords):
            empty_row = r
            break
    if empty_row == 0: empty_row = max(r for r,_,_ in cluster_coords) + 1

    min_row_mirrored = min(r for r, _, _ in cluster)
    row_offset = empty_row - min_row_mirrored

    for r, c, color in cluster:
      new_r = r + row_offset
      if new_r < rows:
        translated_cluster.append((new_r,c,color))
    
    return translated_cluster

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    # initialize output_grid
    grid = np.array(input_grid)
    output_grid = np.zeros_like(grid)

    # Find the top-left cluster
    cluster, _ = find_cluster(grid)

    # Find pixel of color 5
    pixel_5 = find_pixel(grid, 5)

    # Mirror the cluster
    mirrored_cluster = mirror_cluster(cluster)

    # Translate the mirrored cluster
    translated_cluster = translate_cluster(mirrored_cluster, grid)

    # remove pixel 5 and place cluster
    for r, c, color in translated_cluster:
        output_grid[r, c] = color

    return output_grid.tolist()
```
