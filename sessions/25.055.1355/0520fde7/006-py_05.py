"""
1.  **Identify Input Grid Height:** Determine the height of the input grid.
2.  **Create Output Grid:** Create an output grid with the same height as the input grid and a fixed width of 3. Fill the grid with white (0) pixels.
3.  **Place Red Pixel:** In the output grid, place a single red (2) pixel. The row position of this pixel corresponds to the row in the input grid that contains gray (5) pixels. The column position of the red pixel is always 1 (the center column of the 3-wide output grid).
"""

import numpy as np

def find_gray_row(grid):
    # Find the row index containing gray (5) pixels.
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 5:
                return i
    return -1  # Return -1 if no gray pixel is found

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the row containing the gray pixel
    center_row = find_gray_row(input_grid)

    # Initialize the output grid with height same as input, width 3, filled with white (0)
    output_grid = np.zeros((input_grid.shape[0], 3), dtype=int)
    
    # determine center row and column
    center_col = 1

    # if we found a center row, set it in the output grid
    if (center_row != -1):
        output_grid[center_row, center_col] = 2

    return output_grid.tolist()