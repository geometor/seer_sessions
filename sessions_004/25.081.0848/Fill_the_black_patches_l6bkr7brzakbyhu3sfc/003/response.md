```python
"""
Replaces zero-valued pixels in a grid with the most frequent non-zero color among their immediate neighbors (up, down, left, right).
"""

import numpy as np
from collections import Counter

def get_neighbor_colors(grid, row, col):
    """Gets the colors of the immediate neighbors (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = {}

    if row > 0:
        neighbors[(row - 1, col)] =  grid[row - 1, col] # Up
    if row < rows - 1:
        neighbors[(row + 1, col)] = grid[row + 1, col] # Down
    if col > 0:
        neighbors[(row, col-1)] = grid[row, col - 1] # Left
    if col < cols - 1:
        neighbors[(row, col + 1)] = grid[row, col + 1] # Right
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 0:
                # Get the colors of the immediate neighbors.
                neighbor_colors = get_neighbor_colors(input_grid, row, col)

                # Count the occurrences of each neighboring color.
                neighbor_values = list(neighbor_colors.values())
                color_counts = Counter(neighbor_values)

                # Remove 0 from consideration
                if 0 in color_counts:
                    del color_counts[0]

                # Find the most frequent non-zero color.
                if len(color_counts) > 0:
                    most_common_color = color_counts.most_common(1)[0][0]
                    output_grid[row, col] = most_common_color

    return output_grid
```