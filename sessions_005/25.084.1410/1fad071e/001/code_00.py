"""
This program counts the number of 2x2 squares composed entirely of blue pixels (color 1) in the input grid. 
It then generates a 1x5 output grid where the first N cells are blue (1), corresponding to the count N of blue squares found, and the remaining cells are white (0). If the count exceeds 5, only the first 5 cells are blue.
"""

import numpy as np

def find_2x2_squares(grid, color):
    """
    Finds all occurrences of 2x2 squares of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color to search for.

    Returns:
        int: The count of 2x2 squares of the specified color.
    """
    count = 0
    height, width = grid.shape
    # Iterate through possible top-left corners of a 2x2 square
    for r in range(height - 1):
        for c in range(width - 1):
            # Check if the 2x2 square starting at (r, c) consists entirely of the target color
            if (grid[r, c] == color and
                grid[r + 1, c] == color and
                grid[r, c + 1] == color and
                grid[r + 1, c + 1] == color):
                count += 1
    return count

def transform(input_grid):
    """
    Transforms the input grid by counting blue 2x2 squares and representing the count 
    in a 1x5 output grid.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed 1x5 output grid.
    """
    # Convert input list of lists to a numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)

    # Count the number of 2x2 blue squares (color 1)
    blue_square_count = find_2x2_squares(grid_np, 1)

    # Initialize the output grid (1x5) with white pixels (color 0)
    output_grid_np = np.zeros((1, 5), dtype=int)

    # Determine the number of blue pixels to place in the output grid
    # Cap the count at 5, the width of the output grid
    num_blue_pixels = min(blue_square_count, 5)

    # Fill the first 'num_blue_pixels' cells of the output grid with blue (color 1)
    output_grid_np[0, :num_blue_pixels] = 1

    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_grid_np.tolist()

    return output_grid