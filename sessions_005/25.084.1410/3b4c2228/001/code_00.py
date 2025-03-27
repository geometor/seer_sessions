"""
Transformation Rule:
1. Identify and count all distinct occurrences of 2x2 squares composed entirely of green (3) pixels within the input grid.
2. Initialize a 3x3 output grid filled with white (0) pixels.
3. Determine the number of blue (1) pixels to place on the main diagonal (top-left to bottom-right) of the output grid. This number is the minimum of the count of 2x2 green squares and 3.
4. Place the calculated number of blue (1) pixels sequentially along the main diagonal of the output grid, starting from position (0, 0).
5. Return the resulting 3x3 output grid. Red (2) pixels and incomplete green shapes in the input are ignored.
"""

import numpy as np

def _find_green_squares(grid):
    """
    Counts the number of 2x2 green squares in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        int: The count of 2x2 green squares.
    """
    height, width = grid.shape
    count = 0
    # Iterate through possible top-left corners of a 2x2 square
    for r in range(height - 1):
        for c in range(width - 1):
            # Check if the 2x2 block starting at (r, c) is all green (3)
            if (grid[r, c] == 3 and
                grid[r+1, c] == 3 and
                grid[r, c+1] == 3 and
                grid[r+1, c+1] == 3):
                count += 1
    return count

def transform(input_grid):
    """
    Transforms the input grid based on the count of 2x2 green squares.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 3x3 numpy array representing the transformed output grid.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # 1. Initialize a 3x3 output grid filled with white (0) pixels
    output_grid = np.zeros((3, 3), dtype=int)

    # 2. Count the 2x2 green squares in the input grid
    green_square_count = _find_green_squares(input_grid)

    # 3. Determine the number of blue pixels to place (max 3)
    num_blue = min(green_square_count, 3)

    # 4. Place blue (1) pixels on the main diagonal
    for i in range(num_blue):
        output_grid[i, i] = 1 # blue

    # 5. Return the completed output grid
    return output_grid
