# a740d043 • 011 • refine_coder

---
```python
"""
The task involves extracting non-blue (non-1) colored clusters from the input grid and arranging them vertically in the output grid.  The clusters maintain their original colors and relative widths.  A single row of black (0) pixels separates each cluster in the output.  The output grid's height is determined by the sum of the heights of the extracted clusters plus the number of separators.
"""

import numpy as np

def find_clusters(grid):
    # Find clusters of adjacent non-blue pixels
    visited = np.zeros_like(grid, dtype=bool)
    clusters = []

    def dfs(r, c, cluster_colors):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] == 1):
            return []

        visited[r, c] = True
        cluster_colors.add(grid[r,c])
        current_cluster = [(r, c, grid[r, c])]

        current_cluster.extend(dfs(r + 1, c, cluster_colors))
        current_cluster.extend(dfs(r - 1, c, cluster_colors))
        current_cluster.extend(dfs(r, c + 1, cluster_colors))
        current_cluster.extend(dfs(r, c - 1, cluster_colors))
        return current_cluster

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 1 and not visited[r, c]:
                cluster_colors = set()
                cluster = dfs(r, c, cluster_colors)
                if cluster:
                    clusters.append(cluster)
    return clusters

def get_cluster_bounds(cluster):
    # find min and max row and col
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')

    for r, c, _ in cluster:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return min_r, min_c, max_r, max_c

def transform(input_grid):
    input_grid = np.array(input_grid)
    clusters = find_clusters(input_grid)

    # Determine output dimensions
    max_width = 0
    total_height = 0
    for cluster in clusters:
        min_r, min_c, max_r, max_c = get_cluster_bounds(cluster)
        width = max_c - min_c + 1
        height = max_r - min_r + 1
        max_width = max(max_width, width)
        total_height += height

    # Add space for separators
    num_separators = max(0, len(clusters) - 1)  # Avoid negative separators
    total_height += num_separators

    # initialize output_grid
    output_grid = np.zeros((total_height, max_width), dtype=int)

    # Stack clusters vertically
    current_row = 0
    for cluster in clusters:
        min_r, min_c, max_r, max_c = get_cluster_bounds(cluster)
        width = max_c - min_c + 1
        height = max_r - min_r + 1

        # change output pixels
        for r in range(height):
            for c in range(width):
                output_grid[current_row + r, c] = input_grid[min_r + r, min_c + c]
        current_row += height

        # Add separator
        if num_separators > 0:
            current_row += 1  # Separator row
            num_separators -= 1


    return output_grid
```

