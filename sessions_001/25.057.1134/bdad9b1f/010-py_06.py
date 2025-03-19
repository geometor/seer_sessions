"""
1.  **Azure Object:** If an azure (8) object exists (initially a vertical line), extend it downwards. The extension stops at the bottom of the grid OR until one row before a red object. If no red object is present, extend to the bottom.

2.  **Red Object:** If a red (2) object exists (initially a horizontal line), find its original leftmost x coordinate. Replace the leftmost red pixel with a yellow (4) pixel.

3.  **Red Object Expansion (Conditional):** Then, extend the red object to the left and right edges of the grid *on the same row*.

4. **Handle Missing Objects**: Ensure that the transformation handles cases where either the azure or red object (or both) are not present in the input.

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
            stop_row = np.min(red_coords[:, 0]) -1
        else:
            stop_row = rows

        for row in range(min_azure_row, stop_row):
            grid[row, max_azure_col] = 8

def modify_red(grid, red_coords):
   """Modifies the red object, adding yellow and extending."""
   rows, cols = grid.shape
   if len(red_coords) > 0:
        min_red_row = np.min(red_coords[:, 0])
        min_red_col = np.min(red_coords[:, 1])

        # Replace leftmost red with yellow
        grid[min_red_row, min_red_col] = 4
        
        # expand to full width
        for col in range(0, cols):
            if col != min_red_col: # don't overwrite
               grid[min_red_row, col] = 2

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find object coordinates
    azure_coords = find_object(input_grid, 8)
    red_coords = find_object(input_grid, 2)

    # 1. Azure Object Extension
    extend_azure(output_grid, azure_coords, red_coords)

    # 2 & 3. Red Object Modification and Expansion
    modify_red(output_grid, red_coords)


    return output_grid