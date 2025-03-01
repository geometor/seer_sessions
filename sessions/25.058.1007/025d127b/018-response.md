# 025d127b • 018 • refine_coder

---
```python
"""
Identify all disconnected azure (8) shapes within the input grid. For each of these shapes, find the top-right pixel. Preserve these top-right pixels. Change all other azure pixels in the entire grid to white (0).
"""

import numpy as np

def find_azure_shapes(grid):
    """Finds all disconnected azure shapes and returns a list of their coordinates."""
    azure_pixels = np.argwhere(grid == 8)
    if azure_pixels.size == 0:
        return []

    shapes = []
    visited = set()

    for start_pixel in azure_pixels:
        start_tuple = tuple(start_pixel)
        if start_tuple not in visited:
            shape_coords = set()
            stack = [start_tuple]

            while stack:
                current_pixel = stack.pop()
                if current_pixel in visited:  # added to correctly handle edge cases and improve robustness
                    continue
                shape_coords.add(current_pixel)
                visited.add(current_pixel)

                row, col = current_pixel
                neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

                for neighbor_row, neighbor_col in neighbors:
                    if (0 <= neighbor_row < grid.shape[0] and
                        0 <= neighbor_col < grid.shape[1] and
                        grid[neighbor_row, neighbor_col] == 8 and
                        (neighbor_row, neighbor_col) not in visited):
                        stack.append((neighbor_row, neighbor_col))
            shapes.append(list(shape_coords))

    return shapes

def find_top_right_corner(shape_coords):
    """Finds the top-right corner pixel within the shape coordinates."""
    if not shape_coords:
        return None

    max_col = max(coord[1] for coord in shape_coords)
    top_right_candidates = [coord for coord in shape_coords if coord[1] == max_col]
    top_right_corner = min(top_right_candidates, key=lambda coord: coord[0])
    return top_right_corner

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)
    azure_shapes = find_azure_shapes(output_grid)

    # If there are no azure shapes, return the input grid as is.
    if not azure_shapes:
        return output_grid

    # Iterate through each shape
    for shape in azure_shapes:
        # Find top-right corner of the current shape
        top_right_corner = find_top_right_corner(shape)

        # Clear all azure pixels in this shape except the top-right corner
        for r, c in shape:
            if (r, c) != top_right_corner:
                output_grid[r, c] = 0

    return output_grid
```
