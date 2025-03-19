"""
Identifies a red cross in the input grid. The background white pixels to the right of the vertical red line are changed to azure, and the rest of the white pixels are changed to blue.
"""

import numpy as np

def find_red_cross_vertical_arm(grid):
    # Find all red pixels
    red_pixels = np.argwhere(grid == 2)

    # Find the vertical arm: Find range for rows
    if len(red_pixels) > 0:
        min_row = np.min(red_pixels[:, 0])
        max_row = np.max(red_pixels[:, 0])
    
        # Find the column that defines the vertical arm by checking for contiguous red pixels
        vertical_arm_col = -1
        for col in np.unique(red_pixels[:, 1]):
            contiguous_pixels = []
            for row in range(min_row, max_row + 1):
                if grid[row, col] == 2:
                  contiguous_pixels.append( (row, col) )

            if len(contiguous_pixels) == (max_row - min_row + 1):
                vertical_arm_col = col
                break
        return vertical_arm_col

    return -1

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the column index of the vertical arm of the red cross
    vertical_arm_col = find_red_cross_vertical_arm(input_grid)
    
    if (vertical_arm_col >= 0):
        # Iterate through the grid and change colors based on the position relative to the vertical arm
        for r in range(rows):
            for c in range(cols):
                if input_grid[r, c] == 0:  # If it's white
                    if c > vertical_arm_col:
                        output_grid[r, c] = 8  # Change to azure
                    else:
                        output_grid[r, c] = 1  # Change to blue
    return output_grid