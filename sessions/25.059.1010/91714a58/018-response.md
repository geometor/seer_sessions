# 91714a58 • 018 • refine_coder

---
```python
"""
Identifies the largest contiguous cluster of a specific color in the input grid and reproduces it in the output grid, setting all other pixels to 0. The target color appears to vary between examples, so this version attempts to infer it from the input.
"""

import numpy as np

def find_largest_cluster(grid, target_color):
    """
    Finds the largest contiguous cluster of a target color in a grid.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    max_cluster = []

    def dfs(row, col):
        """Depth-First Search to find contiguous pixels."""
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != target_color
        ):
            return []

        visited[row, col] = True
        cluster = [(row, col)]

        cluster.extend(dfs(row + 1, col))
        cluster.extend(dfs(row - 1, col))
        cluster.extend(dfs(row, col + 1))
        cluster.extend(dfs(row, col - 1))
        return cluster

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_color and not visited[r, c]:
                current_cluster = dfs(r, c)
                if len(current_cluster) > len(max_cluster):
                    max_cluster = current_cluster

    return max_cluster

def infer_target_color(grid):
    """
    Infers the target color from the input grid by finding the color of the largest cluster.
    This is a heuristic and may need refinement.
    """
    unique_colors = np.unique(grid)
    max_cluster_size = 0
    target_color = 0  # Default to black if no clusters found

    for color in unique_colors:
        if color == 0:  # Skip background
            continue
        cluster = find_largest_cluster(grid, color)
        if len(cluster) > max_cluster_size:
            max_cluster_size = len(cluster)
            target_color = color

    return target_color

def transform(input_grid):
    # Initialize output_grid with all zeros
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Infer the target color
    target_color = infer_target_color(input_grid)

    # Find the largest cluster of the target color
    largest_cluster = find_largest_cluster(input_grid, target_color)

    # Reconstruct the largest cluster in the output grid
    for row, col in largest_cluster:
        output_grid[row, col] = target_color

    return output_grid
```
