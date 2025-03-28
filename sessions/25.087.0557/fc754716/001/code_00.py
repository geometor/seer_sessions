"""
Identify the single non-white pixel in the input grid. Determine its color.
Create an output grid of the same dimensions as the input grid.
Fill the border (top row, bottom row, leftmost column, rightmost column) of the output grid with the identified color.
Fill the interior of the output grid with white (0).
"""

import numpy as np

def find_non_white_pixel_color(grid):
    """
    Scans the grid to find the color of the single pixel that is not white (0).
    Assumes there is exactly one such pixel.
    """
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0:
                return grid[r, c]
    # Should ideally not be reached given the task constraints
    return 0 # Default to white if no non-white pixel found (error case)

def transform(input_grid):
    """
    Transforms the input grid by creating a frame of the non-white pixel's color.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)

    # 1. Identify the dimensions (height H, width W) of the input grid.
    height, width = input_grid_np.shape

    # 2. Scan the input grid to find the single non-white pixel's color (C).
    frame_color = find_non_white_pixel_color(input_grid_np)

    # 3. Create a new output grid with the same dimensions (H x W), initialized to white (0).
    output_grid = np.zeros((height, width), dtype=int)

    # 4. Iterate through each cell and apply color based on position:
    #    a. If the cell is on the border, set its color to C.
    #    b. Otherwise, it remains white (0) (already initialized).

    # Set top row
    if height > 0:
        output_grid[0, :] = frame_color
    # Set bottom row
    if height > 1:
        output_grid[height - 1, :] = frame_color
    # Set leftmost column
    if width > 0:
        output_grid[:, 0] = frame_color
    # Set rightmost column
    if width > 1:
        output_grid[:, width - 1] = frame_color

    # 5. Return the newly created grid as a list of lists.
    return output_grid.tolist()
