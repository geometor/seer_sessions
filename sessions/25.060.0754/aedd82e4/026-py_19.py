"""
1.  **Red Pixel Preservation:** All red pixels in the input grid remain red in the output grid.
2.  **Center Pixel Transformation (Conditional):** If the center pixel of the input grid is red, it is changed to blue in the output grid. Otherwise, the center pixel remains unchanged.
3.  **White to Blue Conversion (Orthogonally Adjacent to Red):** Any white pixel that is *orthogonally adjacent* (horizontally or vertically, *not* diagonally) to a red pixel in the *input* grid is changed to blue in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the center coordinates
    center_row = rows // 2
    center_col = cols // 2

    # Find all red pixel coordinates in the input grid
    red_pixels = np.argwhere(input_grid == 2)

    # Center Pixel Transformation
    if input_grid[center_row, center_col] == 2:
        output_grid[center_row, center_col] = 1

    # Iterate through all red pixels
    for red_row, red_col in red_pixels:
        # Iterate through orthogonally adjacent cells
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Right, Left, Down, Up
            new_row, new_col = red_row + dr, red_col + dc
            # Check boundaries
            if 0 <= new_row < rows and 0 <= new_col < cols:
                # Check if the adjacent cell is white
                if input_grid[new_row, new_col] == 0:
                    output_grid[new_row, new_col] = 1  # Change to blue

    return output_grid