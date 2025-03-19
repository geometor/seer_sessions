"""
Identify "H" shapes in the grid. An "H" consists of two vertical bars of equal height, connected by a horizontal bar. Locate the central 2x2 block of the "H" and recolor it red. If no "H" is found, return the original grid.
"""

import numpy as np

def find_h_shape(grid):
    gray_pixels = np.argwhere(grid == 5)
    if len(gray_pixels) == 0:
        return None

    min_row = np.min(gray_pixels[:, 0])
    max_row = np.max(gray_pixels[:, 0])
    min_col = np.min(gray_pixels[:, 1])
    max_col = np.max(gray_pixels[:, 1])

    height = max_row - min_row + 1
    width = max_col - min_col + 1

    if height < 3 or width < 3:  # Minimum size for an "H"
        return None

    # Check for two vertical bars
    left_bar = []
    right_bar = []
    for r in range(min_row, max_row + 1):
        if grid[r, min_col] == 5:
            left_bar.append(r)
        if grid[r, max_col] == 5:
            right_bar.append(r)

    if len(left_bar) != height or len(right_bar) != height:
        return None

    # Check for a connecting horizontal bar
    center_row = (min_row + max_row) // 2
    horizontal_bar_length = 0
    for c in range(min_col + 1, max_col):
        if grid[center_row, c] == 5:
            horizontal_bar_length += 1

    if horizontal_bar_length == 0:
       # Check other rows for horizontal bar
        for r in range(min_row + 1, max_row):
            horizontal_bar_length = 0
            for c in range(min_col + 1, max_col):
                if grid[r, c] == 5:
                    horizontal_bar_length += 1
            if horizontal_bar_length >0:
                center_row = r #update center row
                break

    if horizontal_bar_length == 0: #still zero
        return None


    center_col = (min_col + max_col) // 2
    return center_row, center_col



def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the center of the "H" shape
    center_coords = find_h_shape(output_grid)

    if center_coords:
        center_row, center_col = center_coords
        # Recolor the 2x2 center region to red (2)
        output_grid[center_row-1:center_row+1, center_col:center_col+2] = 2
        if output_grid.shape[1] - center_col <2: #check if it can contain 2x2
            output_grid[center_row-1:center_row+1, center_col-1:center_col+1] = 2
        if output_grid.shape[0] - center_row + 1<2: #check if it can contain 2x2 for rows
            output_grid[center_row-1:center_row, center_col:center_col+2] = 2 #redefine the range

    return output_grid