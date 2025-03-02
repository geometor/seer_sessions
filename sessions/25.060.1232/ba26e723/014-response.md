# ba26e723 • 014 • refine_coder

---
```python
"""
Transforms yellow pixels to magenta if they are adjacent to at least one white pixel, excluding yellow pixels within a 2x2 yellow square.
"""

import numpy as np

def is_part_of_2x2_yellow_square(grid, r, c):
    """
    Checks if the pixel at (r, c) is part of a 2x2 square of only yellow pixels.
    """
    if grid[r,c] != 4:
        return False

    for r_start in [r - 1, r]:
        for c_start in [c - 1, c]:
            if all(0 <= r_start + dr < grid.shape[0] and 0 <= c_start + dc < grid.shape[1] and grid[r_start + dr, c_start + dc] == 4 for dr in range(2) for dc in range(2)):
                return True
    return False

def transform(input_grid):
    """
    Transforms the input grid by changing yellow pixels to magenta based on adjacency to white pixels.
    """
    output_grid = np.copy(input_grid)

    # Iterate through all pixels
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            # Check if the pixel is yellow
            if output_grid[r, c] == 4:
                # Check for adjacency to white pixels
                adjacent_to_white = False
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < output_grid.shape[0] and 0 <= nc < output_grid.shape[1] and output_grid[nr, nc] == 0:
                        adjacent_to_white = True
                        break
                # if adjacent to white and it is not part of 2x2 yellow block
                if adjacent_to_white and not is_part_of_2x2_yellow_square(output_grid,r,c):
                    output_grid[r, c] = 6

    return output_grid
```
