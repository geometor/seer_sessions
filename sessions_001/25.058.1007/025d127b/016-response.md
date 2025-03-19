# 025d127b • 016 • refine_coder

---
```python
"""
Identify a connected shape of azure (8) pixels within the input grid. Preserve the top-right corner of the shape. Clear all other azure pixels to white (0).
"""

import numpy as np

def get_azure_shape(grid):
    """Finds the connected azure shape and returns its coordinates."""
    azure_pixels = np.argwhere(grid == 8)
    if azure_pixels.size == 0:
        return []

    # Create a set for easier membership checking and to avoid duplicates
    shape_coords = set()

    # Start with the first azure pixel found
    stack = [tuple(azure_pixels[0])]

    while stack:
        current_pixel = stack.pop()
        shape_coords.add(current_pixel)

        # Check neighbors (up, down, left, right)
        row, col = current_pixel
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

        for neighbor_row, neighbor_col in neighbors:
            if (0 <= neighbor_row < grid.shape[0] and
                0 <= neighbor_col < grid.shape[1] and
                grid[neighbor_row, neighbor_col] == 8 and
                (neighbor_row, neighbor_col) not in shape_coords):
                stack.append((neighbor_row, neighbor_col))
    return list(shape_coords)

def find_top_right_corner(shape_coords):
    """Finds the top-right corner pixel within the shape coordinates."""
    if not shape_coords:
        return None

    # Find the maximum column index
    max_col = max(coord[1] for coord in shape_coords)

    # Filter pixels with the maximum column index and find minimum row index
    top_right_candidates = [coord for coord in shape_coords if coord[1] == max_col]
    top_right_corner = min(top_right_candidates, key=lambda coord: coord[0])

    return top_right_corner

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)
    azure_shape_coords = get_azure_shape(output_grid)

    # If there's no azure shape, return the input grid as is
    if not azure_shape_coords:
      return output_grid

    # Find the top-right corner
    top_right_corner = find_top_right_corner(azure_shape_coords)

    # Create a set for quick lookup
    azure_set = set(azure_shape_coords)

    # Iterate through azure shape and clear other pixels
    for r, c in azure_set:
        if (r, c) != top_right_corner:
            output_grid[r, c] = 0

    return output_grid
```
