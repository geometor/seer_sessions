```python
"""
1.  **Input:** Receive a 2D grid of integers (0-9), where each integer represents a color.

2.  **Cluster Identification:** Identify all distinct clusters of azure (8) colored pixels.  Pixels are part of the same cluster if they are directly adjacent horizontally or vertically (not diagonally).

3.  **Extrema Identification (Revised):** Within each identified azure cluster:
    *   **Top-Left:** Find all pixels with minimum row. Of those, find the one the smallest column.
    *   **Top-Right:** Find all pixels with the minimum row. Of those, find the one with the largest column.
    *   **Bottom-Left:** Find all pixels with the maximum row. Of those, find the one with the smallest column.
    *   **Bottom-Right:** Find all pixels with maximum row, and of those, find the one with maximum column.

4.  **Color Transformation:** Change the colors of the identified extrema pixels as follows:
    *   Top-Left pixel: Change to blue (1).
    *   Top-Right pixel: Change to yellow (4).
    *   Bottom-Left pixel: Change to green (3).
    *   Bottom-Right pixel: Change to red (2).

5.  **Preservation:** Ensure all pixels that are *not* azure retain their original color.

6.  **Output:** Return the modified 2D grid with the color transformations applied to the identified extrema pixels within each azure cluster.
"""

import numpy as np

def find_clusters(grid, color):
    """
    Finds clusters of a specific color in the grid.
    """
    visited = set()
    clusters = []

    def is_valid(row, col):
        return 0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]

    def dfs(row, col, current_cluster):
        if (row, col) in visited or not is_valid(row, col) or grid[row, col] != color:
            return

        visited.add((row, col))
        current_cluster.append((row, col))

        # Explore adjacent cells (up, down, left, right)
        dfs(row + 1, col, current_cluster)
        dfs(row - 1, col, current_cluster)
        dfs(row, col + 1, current_cluster)
        dfs(row, col - 1, current_cluster)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_cluster = []
                dfs(row, col, current_cluster)
                clusters.append(current_cluster)

    return clusters

def get_cluster_extrema(cluster):
    """
    Find the top-left, top-right, bottom-left, and bottom-right pixel coordinates of a cluster.
    Revised to handle multiple min/max rows/cols.
    """
    if not cluster:
        return None, None, None, None

    rows, cols = zip(*cluster)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    # Find all pixels with the minimum row
    top_pixels = [(r, c) for r, c in cluster if r == min_row]
    # Top-Left: Minimum row, minimum column among top pixels
    top_left = min(top_pixels, key=lambda x: x[1])
    # Top-Right: Minimum row, maximum column among top pixels
    top_right = max(top_pixels, key=lambda x: x[1])

    # Find all pixels with maximum row
    bottom_pixels = [(r,c) for r,c in cluster if r == max_row]
    # Bottom-Left: Maximum row, minimum column among bottom pixels
    bottom_left = min(bottom_pixels, key=lambda x: x[1])
    # Bottom-Right: Maximum row, maximum column among bottom pixels.
    bottom_right = max(bottom_pixels, key=lambda x: x[1])

    return top_left, top_right, bottom_left, bottom_right


def transform(input_grid):
    """
    Transforms the input grid according to the identified rule.
    """
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()
    
    # Find azure clusters
    azure_clusters = find_clusters(input_grid, 8)
    
    # Iterate through each cluster
    for cluster in azure_clusters:
        # Determine extrema within cluster (refined logic)
        top_left, top_right, bottom_left, bottom_right = get_cluster_extrema(cluster)

        # Transform based on relative position
        output_grid[top_left] = 1      # Top-left -> Blue
        output_grid[top_right] = 4     # Top-right -> Yellow
        output_grid[bottom_left] = 3   # Bottom-left -> Green
        output_grid[bottom_right] = 2  # Bottom-right -> Red
    

    return output_grid.tolist()
```