"""
1. Identify the Frame: Examine the input grid to determine the color of the outermost, continuous layer (the frame).
2. Extract Inner Rectangle: Locate and extract the contiguous inner region (the "inner rectangle") within the input grid, excluding the identified frame.
3. Create the Output Grid: Create a copy of the input grid, maintaining its original dimensions.
4. Clear the Frame: Fill the area corresponding to the original frame in the output grid with black pixels (color 0).
5. Clear outside the Inner Rectangle: Fill the remaining area in the output grid between the edge and the inner rectangle with black pixels.
"""

import numpy as np

def find_frame_color(grid):
    # Get the color of the top-left pixel, assuming it's part of the frame
    return grid[0, 0]

def find_inner_rectangle_bounds(grid, frame_color):
    # Find the boundaries of the inner rectangle
    rows, cols = grid.shape
    top, bottom, left, right = 0, rows - 1, 0, cols - 1

    # Find top boundary
    while top < rows and all(grid[top, :] == frame_color):
        top += 1

    # Find bottom boundary
    while bottom >= 0 and all(grid[bottom, :] == frame_color):
        bottom -= 1

    # Find left boundary
    while left < cols and all(grid[:, left] == frame_color):
        left += 1

    # Find right boundary
    while right >= 0 and all(grid[:, right] == frame_color):
        right -= 1
        
    return top, bottom, left, right

def transform(input_grid):
    # Create a copy of the input grid as the output grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify the frame color
    frame_color = find_frame_color(input_grid)

    # Find the inner rectangle bounds
    top, bottom, left, right = find_inner_rectangle_bounds(input_grid, frame_color)

    # Clear the area outside the inner rectangle (including the frame)
    for i in range(rows):
        for j in range(cols):
            if i < top or i > bottom or j < left or j > right:
                output_grid[i, j] = 0

    return output_grid