# 0e206a2e • 007 • refine_coder

---
```python
"""
Transforms two clusters of pixels in an input grid to an output grid. The clusters maintain their relative
positions (top-right and bottom-left). The top-right cluster expands horizontally, and the bottom-left cluster
expands vertically. The colors within each cluster are preserved.
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

def analyze_clusters(grid):
    clusters = get_clusters(grid)
    cluster_data = []
    for i, cluster in enumerate(clusters):
        rows, cols, colors = zip(*cluster)
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
        size = len(cluster)
        unique_colors = sorted(list(set(colors)))
        cluster_data.append({
            'cluster_id': i + 1,
            'bounding_box': (min_row, max_row, min_col, max_col),
            'size': size,
            'colors': unique_colors
        })
    return cluster_data

def transform(input_grid):
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_grid)

    # Get clusters and their bounding boxes from the input grid
    clusters = get_clusters(input_grid)
    cluster_data = analyze_clusters(input_grid)


    # Process each cluster
    for i, cluster in enumerate(cluster_data):

        # Get bounding box and colors
        min_row, max_row, min_col, max_col = cluster['bounding_box']
        colors = cluster['colors']

        # Determine relative position (top-right or bottom-left)
        # using simple median of the grid, since there are only two objects
        if min_col > input_grid.shape[1] // 2: # Top-right cluster
            #horizontal expansion
            width = (max_col-min_col+1) * 2 if (max_col-min_col+1) %2 != 0 else (max_col-min_col+1)
            for r in range(3):
              for c in range(width):
                color_index = (r* width + c) % len(colors)
                output_grid[r+2, (output_grid.shape[1]-width) + c] = colors[color_index]


        else: # Bottom-left cluster
            # vertical expansion
            height = (max_row-min_row+1) * 2 if (max_row-min_row+1) %2 != 0 else (max_row-min_row+1)

            for r in range(height):
                for c in range(max_col - min_col + 1):
                  color_index = (r * (max_col-min_col+1) + c) % len(colors)
                  output_grid[9+r, min_col + c] = colors[color_index]

    return output_grid
```
