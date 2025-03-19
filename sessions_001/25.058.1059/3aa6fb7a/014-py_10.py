"""
The transformation focuses on azure (8) pixels. An azure pixel will only transform if a grey pixel is present in the input grid. An azure pixel will transform to blue (1) if: there is an adjacent grey pixel to the immediate west, and the azure pixel has exactly one azure neighbor. All other pixels remain unchanged.
"""

import numpy as np

def count_adjacent_azure(grid, row, col):
    """Counts the number of adjacent azure pixels (excluding diagonals)."""
    count = 0
    rows, cols = grid.shape
    # Check North
    if row > 0 and grid[row-1, col] == 8:
        count += 1
    # Check South
    if row < rows - 1 and grid[row+1, col] == 8:
        count += 1
    # Check West
    if col > 0 and grid[row, col-1] == 8:
        count += 1
    # Check East
    if col < cols - 1 and grid[row, col+1] == 8:
        count += 1
    return count

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    # check if a grey pixel is present in the input
    grey_present = 5 in input_grid

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check if the pixel is azure
            if input_grid[row, col] == 8:
                # Count adjacent azure pixels
                adjacent_azure_count = count_adjacent_azure(input_grid, row, col)
                #check for grey to the west
                grey_to_west = False
                if col > 0 and input_grid[row,col-1] == 5:
                    grey_to_west = True

                # Conditional transformation
                if grey_present and grey_to_west and adjacent_azure_count == 1:
                    output_grid[row,col] = 1

    return output_grid