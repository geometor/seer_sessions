# 3ac3eb23 • 008 • refine_coder

---
```python
"""
1.  **Identify Seed Pixels:** Locate all red (2) and azure (8) pixels in the input grid. These are the "seed" pixels.

2.  **Propagate Colors:** For each seed pixel (red or azure):
    *   Propagate the seed pixel's color downwards, diagonally down-left, and diagonally down-right.
    *   Continue propagation in each direction in single-pixel steps.
    *  Stop propagation in a given direction if:
        *   The edge of the grid is reached.
        *   The target cell is *not* white (0). This includes both originally non-white pixels and pixels that have become non-white due to propagation.

3.  **Output:** Return the resulting grid. The propagation overlays onto the existing grid, without changing any of the original non-white pixels. The key difference from the previous program is the explicit stopping condition: propagation stops not only at original non-white pixels but *also at any propagated pixels*.
"""

import numpy as np

def get_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specified color."""
    return np.argwhere(grid == color)

def propagate_color(grid, start_row, start_col, color):
    """Propagates a color downwards and diagonally, stopping at non-white pixels."""
    rows, cols = grid.shape
    queue = [(start_row, start_col)]

    while queue:
        r, c = queue.pop(0)

        # Propagate down
        if r + 1 < rows and grid[r + 1, c] == 0:
            grid[r + 1, c] = color
            queue.append((r + 1, c))

        # Propagate down-left
        if r + 1 < rows and c - 1 >= 0 and grid[r + 1, c - 1] == 0:
            grid[r + 1, c - 1] = color
            queue.append((r + 1, c - 1))

        # Propagate down-right
        if r + 1 < rows and c + 1 < cols and grid[r + 1, c + 1] == 0:
            grid[r + 1, c + 1] = color
            queue.append((r + 1, c + 1))


def transform(input_grid):
    """Transforms the input grid according to the propagation rule."""
    output_grid = np.copy(input_grid)

    # Propagate red pixels
    for row, col in get_pixels_by_color(input_grid, 2):
        propagate_color(output_grid, row, col, 2)

    # Propagate azure pixels
    for row, col in get_pixels_by_color(input_grid, 8):
        propagate_color(output_grid, row, col, 8)

    return output_grid
```
