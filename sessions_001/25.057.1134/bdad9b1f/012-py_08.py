"""
1.  **Identify Objects:** Find the azure (8) vertical line and the red (2) horizontal line. If either is missing, skip the corresponding steps.

2.  **Extend Azure:** If an azure object exists, extend it downwards. The extension stops at the bottom of the grid or one row above any red object.

3.  **Expand Red:** If a red object exists, first expand the red object horizontally to the left and right edges of the grid on the same row.

4.  **Modify Red:** After expanding, replace the original leftmost pixel of the red object with a yellow (4) pixel.

5.  **Background:** All other pixels remain white (0).
"""

import numpy as np

def find_object(grid, color):
    """Finds coordinates of pixels with the specified color."""
    coords = np.argwhere(grid == color)
    return coords

def extend_azure(grid, azure_coords, red_coords):
    """Extends the azure object downwards."""
    rows, _ = grid.shape
    if len(azure_coords) > 0:
        min_azure_row = np.min(azure_coords[:, 0])
        max_azure_col = azure_coords[0][1]

        # Determine stop row (bottom of grid or row before red object)
        if len(red_coords) > 0:
            stop_row = np.min(red_coords[:, 0]) - 1
        else:
            stop_row = rows

        for row in range(min_azure_row, stop_row):
            grid[row, max_azure_col] = 8

def expand_and_modify_red(grid, red_coords):
    """Expands the red object and then modifies the leftmost pixel."""
    rows, cols = grid.shape
    if len(red_coords) > 0:
        min_red_row = np.min(red_coords[:, 0])
        original_min_red_col = np.min(red_coords[:, 1])

        # Expand to full width
        for col in range(0, cols):
            grid[min_red_row, col] = 2

        # Replace original leftmost red with yellow
        grid[min_red_row, original_min_red_col] = 4


def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    output_grid = np.copy(input_grid)

    # Find object coordinates
    azure_coords = find_object(input_grid, 8)
    red_coords = find_object(input_grid, 2)

    # 1. Azure Object Extension
    extend_azure(output_grid, azure_coords, red_coords)

    # 2 & 3. Red Object Expansion and Modification (Corrected Order)
    expand_and_modify_red(output_grid, red_coords)

    return output_grid