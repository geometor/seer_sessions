# 4093f84a • 014 • refine_coder

---
```python
"""
The transformation rule removes green (3) pixels from the input grid under specific conditions:

1. Green pixels that have at least one non-green neighbor are removed, and in their place in the output grid is the color of one such neighbor.
2. If a green pixel has multiple non-green neighbors, the neighbor color that is used to replace it is determined not by priority, but by simply copying whatever color is found in the grid, as long there is only one.
3.  If all neighbors are the same, then the green is replaced by that single color.
4. If a green pixel is surrounded entirely by green pixels or the boundary, then change it to white (0).

"""

import numpy as np

def get_neighbor_colors(grid, r, c):
    """Gets the colors of the immediate neighbors of a pixel."""
    rows, cols = grid.shape
    neighbor_colors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbor_colors.append(grid[nr, nc])
    return neighbor_colors

def transform(input_grid):
    """
    Transforms the input grid by removing green pixels based on their neighbors.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    green_pixels = np.where(input_grid == 3)
    green_coords = list(zip(green_pixels[0], green_pixels[1]))

    for r, c in green_coords:
        neighbor_colors = get_neighbor_colors(input_grid, r, c)
        non_green_neighbors = [color for color in neighbor_colors if color != 3]

        if non_green_neighbors:
            # Check if all non-green neighbors are the same color
            unique_non_green = list(set(non_green_neighbors))
            if len(unique_non_green) == 1:
                output_grid[r, c] = unique_non_green[0]

        else:
            # If no non-green neighbors, change to white.
            output_grid[r, c] = 0

    return output_grid
```
