"""
1.  **Identify Target Pixels:** Iterate through each pixel in the input grid.
2.  **Check for 8s:**. Look for azure pixels (value 8).
3.  **Conditional Replacement:**
    *   If an azure (8) pixel is found, check if it's adjacent (horizontally or vertically) to another azure (8) pixel.
        *   if two or more azure pixels (8) are adjacent (either horizontal or vertical, no diagonals) replace all adjacent azure pixels (8) with gray (5).
    *   If an azure pixel (8) is present but not adjacent to another azure pixel (8), Check these other conditions:
       * If a lonely azure (8) is in the same row with another pixel value 1 or 3, change the lonely (8) to gray (5).
       * If a lonely azure (8) is in the same column with another pixel value 1 or 3, do NOT change this (8)
       * otherwise, change that lonely azure pixel (8) with gray (5)

4.  **Output:** Create a new grid with the modified pixel colors, leaving all other pixels unchanged.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """Gets the values of horizontally and vertically adjacent pixels."""
    adjacent = []
    rows, cols = grid.shape
    if row > 0:
        adjacent.append(grid[row-1, col])  # Up
    if row < rows - 1:
        adjacent.append(grid[row+1, col])  # Down
    if col > 0:
        adjacent.append(grid[row, col-1])  # Left
    if col < cols - 1:
        adjacent.append(grid[row, col+1])  # Right
    return adjacent
    
def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check for 8s
            if input_grid[row, col] == 8:
                adjacent_pixels = get_adjacent_pixels(input_grid, row, col)
                # Conditional Replacement
                if 8 in adjacent_pixels:
                    # if two or more azure pixels (8) are adjacent replace with gray (5).
                    output_grid[row,col] = 5
                else:
                    # Check other conditions for lone 8s
                    row_values = input_grid[row, :]
                    if 1 in row_values or 3 in row_values:
                         output_grid[row, col] = 5
                    elif not(1 in input_grid[:,col] or 3 in input_grid[:,col]):
                         output_grid[row,col] = 5
    return output_grid