"""
1. **Find Subgrid:** Scan the input grid to locate a 3x3 subgrid where the center pixel's color is different from all the surrounding pixels' color. All surrounding pixels must have the same color.
2. **Recolor Subgrid:** Once the subgrid is found, change the color of all the surrounding pixels to 2 (red) and the color of the center pixel to 6 (magenta).
3. **Place Subgrid:** Copy this recolored 3x3 subgrid to the output grid.  Place the top-left corner of the subgrid at row 2, column 7 (using 0-based indexing, this is row 1, column 6).
4. **Clear output:** Initialize the output grid by setting every pixel in the output grid to black/0.
5. **Place:** Copy the recolored subgrid to the output.
"""

import numpy as np

def find_subgrid(grid):
    """Finds a 3x3 subgrid with a differently colored center."""
    rows, cols = grid.shape
    for i in range(rows - 2):
        for j in range(cols - 2):
            subgrid = grid[i:i+3, j:j+3]
            center_color = subgrid[1, 1]
            outer_colors = subgrid.flatten()
            outer_colors = outer_colors[outer_colors != center_color]
            if len(outer_colors) > 0 and np.all(outer_colors == outer_colors[0]):
                # All outer colors are the same and different from the center.
                return i, j
    return None, None

def transform(input_grid):
    # Initialize output_grid to all zeros.
    output_grid = np.zeros_like(input_grid)

    # Find the subgrid in the input.
    row_start, col_start = find_subgrid(input_grid)

    # Check if a subgrid was found
    if row_start is not None and col_start is not None:
        # Recolor and place the subgrid in the output.
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    output_grid[1 + i, 6 + j] = 6  # Center pixel to magenta (6).
                else:
                    output_grid[1 + i, 6 + j] = 2  # Outer pixels to red (2).

    return output_grid