"""
1.  **Identify Seed Pixels:** Locate all red (2) and azure (8) pixels in the input grid. These are the "seed" pixels for propagation.

2.  **Propagate Red Pixels:** For each red pixel:
    *   Create a red pixel directly beneath it.
    *   Create a red pixel diagonally down and to the left.
    *   Create a red pixel diagonally down and to the right.
    *   Repeat these three sub-steps for all newly created red pixels until a grid boundary is reached or a non-white pixel is encountered.

3.  **Propagate Azure Pixels:** For each azure pixel:
    *   Create an azure pixel directly beneath it.
    *   Create an azure pixel diagonally down and to the left.
    *   Create an azure pixel diagonally down and to the right.
    *   Repeat these three sub-steps for all newly created azure pixels until a grid boundary is reached or a non-white pixel is encountered.

4. **Output**: Return the final grid, which includes the original seed pixels and all propagated pixels, overlaid on the original white background. The propagation does not affect or remove original non-white pixels.
"""

import numpy as np

def get_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specified color."""
    return np.argwhere(grid == color)

def propagate_color(grid, start_row, start_col, color):
    """Propagates a color downwards and diagonally."""
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