# 4c5c2cf0 • 017 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all contiguous clusters of azure (color 8) pixels and green (color 3) pixels.
2.  **Green Center:** Determine the row index of the center of the green cluster. This serves as the reflection axis.
3.  **Expansion:**
    *   Find the distance from the top of the azure object to the top of the grid. Add the same number of rows to the *top* of the azure object.
    *   Find the distance from the bottom of the azure object to the bottom of the grid. Add the same number of rows to the *bottom* of the azure object.
4.  **Reflect Azure:** Reflect the expanded azure cluster across the horizontal axis defined by the center row of the green cluster. The reflected azure cluster will consist of azure (8) pixels.
5.  **Preserve green:** The original green cluster from input remains in same location.
6.  **Output:** Combine the expanded and reflected azure cluster, along with the original green cluster, to create the output grid.
"""

import numpy as np

def find_clusters(grid, color):
    clusters = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_cluster):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_cluster.append((r, c))

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, current_cluster)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_cluster = []
                dfs(r, c, current_cluster)
                clusters.append(current_cluster)
    return clusters

def get_cluster_center(cluster):
    row_sum = sum(r for r, _ in cluster)
    col_sum = sum(c for _, c in cluster)
    center_row = row_sum / len(cluster)
    center_col = col_sum / len(cluster)
    return center_row, center_col

def get_cluster_top_bottom(cluster):
    rows = [r for r, _ in cluster]
    return min(rows), max(rows)

def expand_cluster(cluster, top_dist, bottom_dist, grid_height):
    expanded_cluster = []
    for r, c in cluster:
      expanded_cluster.append((r,c))

    #expand top
    for r, c in cluster:
        new_r = r - top_dist
        if 0 <= new_r:
          expanded_cluster.append( (new_r, c ))

    #expand bottom
    for r,c in cluster:
      new_r = r + bottom_dist
      if new_r < grid_height:
          expanded_cluster.append( (new_r, c))

    return expanded_cluster
    

def reflect_cluster(cluster, axis_row):
    reflected_cluster = []
    for r, c in cluster:
        dist = r - axis_row
        new_r = axis_row - dist
        if 0 <= new_r < 30: # Assuming max grid size of 30x30
          reflected_cluster.append((int(new_r), c))
    return reflected_cluster

def transform(input_grid):
    # Initialize output grid
    output_grid = np.zeros_like(input_grid)

    # Find azure and green clusters
    azure_clusters = find_clusters(input_grid, 8)
    green_clusters = find_clusters(input_grid, 3)

    # Process each azure cluster
    for azure_cluster in azure_clusters:
        # Expansion
        top_row, bottom_row = get_cluster_top_bottom(azure_cluster)
        top_dist = top_row
        bottom_dist = input_grid.shape[0] - 1 - bottom_row
        expanded_azure = expand_cluster(azure_cluster, top_dist, bottom_dist, input_grid.shape[0])


        # Reflection (if green exists)
        if green_clusters:
            green_center_row, _ = get_cluster_center(green_clusters[0])
            reflected_azure = reflect_cluster(expanded_azure, green_center_row)

            # Add reflected azure to output
            for r, c in reflected_azure:
              if 0 <= r < output_grid.shape[0]:
                output_grid[r, c] = 8


        # add expanded azure
        for r, c in expanded_azure:
          if 0 <= r < output_grid.shape[0]:
              output_grid[r,c] = 8

    # Copy green cluster to output
    for green_cluster in green_clusters:
        for r, c in green_cluster:
            output_grid[r, c] = 3

    return output_grid
```
