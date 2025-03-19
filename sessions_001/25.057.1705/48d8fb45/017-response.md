# 48d8fb45 • 017 • refine_coder

---
```python
"""
Finds all red (color 2) objects in the input grid, determines the bounding box
encompassing all red pixels, and crops the input grid to this bounding box.
"""

import numpy as np

def find_object(grid, target_color):
    """
    Finds all contiguous clusters of the target color in the grid.
    Returns a list of bounding box tuples (min_row, max_row, min_col, max_col)
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    visited = set()
    clusters = []

    def dfs(row, col):
        """Depth-First Search to find contiguous pixels of the target color."""
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or (row, col) in visited
            or grid[row][col] != target_color
        ):
            return []

        visited.add((row, col))
        cluster = [(row, col)]

        # Explore adjacent pixels (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                cluster.extend(dfs(row + dr, col + dc))

        return cluster

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == target_color and (r, c) not in visited:
                cluster_pixels = dfs(r, c)
                if cluster_pixels:
                    # Find min/max row and col to define the bounding box
                    min_row = min(pixel[0] for pixel in cluster_pixels)
                    max_row = max(pixel[0] for pixel in cluster_pixels)
                    min_col = min(pixel[1] for pixel in cluster_pixels)
                    max_col = max(pixel[1] for pixel in cluster_pixels)
                    clusters.append((min_row, max_row, min_col, max_col))

    return clusters

def transform(input_grid):
    # Find all red clusters.
    red_clusters = find_object(input_grid, 2)

    # If no red pixels are found, return an empty grid.
    if not red_clusters:
        return [[]]

    # Find the overall bounding box encompassing all red clusters.
    min_row = min(cluster[0] for cluster in red_clusters)
    max_row = max(cluster[1] for cluster in red_clusters)
    min_col = min(cluster[2] for cluster in red_clusters)
    max_col = max(cluster[3] for cluster in red_clusters)

    # Crop the grid.
    cropped_grid = [
        row[min_col : max_col + 1] for row in input_grid[min_row : max_row + 1]
    ]
    return cropped_grid
```
