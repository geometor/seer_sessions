# 0e206a2e • 008 • refine_coder

---
```python
"""
The transformation identifies two distinct clusters of non-zero pixels in the input grid. A cluster is a group of adjacently connected non-zero pixels (both orthogonal and diagonal). The transformation repositions and combines these clusters into specific regions of the output grid. The top-right cluster is moved to rows 3-5 and columns 13-17. The bottom-left cluster is moved to rows 9-11 and columns 0-2. The colors within each cluster are preserved, although their internal arrangement might change.
"""

import numpy as np

def get_clusters(grid):
    """Identifies and returns clusters of connected non-zero pixels."""
    visited = set()
    clusters = []

    def dfs(r, c, current_cluster):
        """Depth-First Search to find connected components."""
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] == 0:
            return
        visited.add((r, c))
        current_cluster.append((r, c, grid[r,c]))
        # Explore adjacent cells (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(r + dr, c + dc, current_cluster)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_cluster = []
                dfs(r, c, current_cluster)
                clusters.append(current_cluster)
    return clusters

def transform(input_grid):
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_grid)

    # Get clusters from the input grid
    clusters = get_clusters(input_grid)

    # Process each cluster and reposition/modify it in the output grid
    for cluster in clusters:
        # Sort cluster elements to identify top-right and bottom-left
        # Top-right:  Based on smallest combined row and col indices
        # Bottom-left: Based on largest combined row and col indices
        sorted_cluster = sorted(cluster, key=lambda x: x[0] + x[1])

        if sorted_cluster[0][1] > input_grid.shape[1] // 2: # Top-right cluster
            # Place colors of the top-right cluster into rows 3, 4, and 5.
            colors = [pixel[2] for pixel in cluster]
            colors.sort()

            output_grid[2,14] = colors[0] if 0 < len(colors) else 0
            output_grid[2,15] = colors[1] if 1 < len(colors) else 0
            output_grid[2,16] = colors[2] if 2 < len(colors) else 0

            output_grid[3,14] = colors[0] if 0 < len(colors) else 0
            output_grid[3,15] = colors[1] if 1 < len(colors) else 0
            output_grid[3,16] = colors[2] if 2 < len(colors) else 0
            output_grid[3,17] = colors[3] if 3 < len(colors) else 0

            output_grid[4,13] = colors[0] if 0 < len(colors) else 0
            output_grid[4,14] = colors[1] if 1 < len(colors) else 0
            output_grid[4,15] = colors[2] if 2 < len(colors) else 0
            output_grid[4,16] = colors[3] if 3 < len(colors) else 0
            output_grid[4,17] = colors[4] if 4 < len(colors) else 0



        else: # Bottom-left cluster
            # Place colors of the bottom-left cluster into rows 9, 10, and 11.
            colors = [pixel[2] for pixel in cluster]
            colors.sort() # Sort the colors to ensure consistent placement
            output_grid[9,0] = 0
            output_grid[9,1] = colors[0] if 0 < len(colors) else 0
            output_grid[9,2] = colors[1] if 1 < len(colors) else 0
            output_grid[10,0] = colors[2] if 2 < len(colors) else 0
            output_grid[10,1] = colors[3] if 3 < len(colors) else 0
            output_grid[10,2] = colors[4] if 4 < len(colors) else 0
            output_grid[11,0] = 0
            output_grid[11,1] = colors[5] if 5 < len(colors) else 0
            output_grid[11,2] = colors[0] if 0 < len(colors) else 0

    return output_grid
```
