"""
Iterates through each pixel of the input grid. Identifies pixels with a value of '0' (white).
For each '0' pixel, checks for adjacent '5' (gray) pixels. 
 - Are there exactly two adjacent '5' valued pixels?
 - Are the adjacent '5' pixels on opposite sides of the '0' pixel (horizontally or vertically)?
If both conditions are true, change the '0' pixel to '2' (red) in the output grid.
Otherwise, copy the input pixel value to the output grid.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """Gets the values of adjacent pixels (up, down, left, right)."""
    rows, cols = grid.shape
    adjacent = []
    if row > 0:
        adjacent.append((row - 1, col, grid[row - 1, col]))  # Up
    if row < rows - 1:
        adjacent.append((row + 1, col, grid[row + 1, col]))  # Down
    if col > 0:
        adjacent.append((row, col - 1, grid[row, col - 1]))  # Left
    if col < cols - 1:
        adjacent.append((row, col + 1, grid[row, col + 1]))  # Right
    return adjacent

def are_opposite(pos1, pos2):
    """Checks if two positions are opposite (horizontal or vertical)."""
    row1, col1, _ = pos1
    row2, col2, _ = pos2
    return (row1 == row2 and col1 != col2) or (row1 != row2 and col1 == col2)

def transform(input_grid):
    """Transforms the input grid according to the adjacency rule."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = np.copy(input_grid)  # Initialize output_grid
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check if the pixel is '0'
            if input_grid[row, col] == 0:
                # Get adjacent pixels
                adjacent = get_adjacent_pixels(input_grid, row, col)
                
                # Filter adjacent pixels with value '5'
                adjacent_5 = [p for p in adjacent if p[2] == 5]
                
                # Check if there are exactly two adjacent '5' pixels
                if len(adjacent_5) == 2:
                    # Check if they are on opposite sides
                    if are_opposite(adjacent_5[0], adjacent_5[1]):
                        # Change '0' to '2'
                        output_grid[row, col] = 2

    return output_grid