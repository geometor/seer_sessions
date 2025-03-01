"""
1. Identify 2x2 Gray Squares: Find all 2x2 squares of gray (5) pixels in the input grid.
2. Check Surroundings: For each identified square, examine the surrounding pixels within a radius of 1 and 2.
3. Conditional Transformation: If *all* surrounding pixels within radius 1 and 2 are black (0), change the color of all pixels within the 2x2 gray square to red (2).
4. Output: Return the modified grid.
"""

import numpy as np

def find_2x2_gray_squares(grid):
    """Finds the top-left coordinates of all 2x2 gray squares in a grid."""
    rows, cols = grid.shape
    squares = []
    for i in range(rows - 1):
        for j in range(cols - 1):
            if (grid[i, j] == 5 and grid[i + 1, j] == 5 and
                grid[i, j + 1] == 5 and grid[i + 1, j + 1] == 5):
                squares.append((i, j))
    return squares

def get_surrounding_pixels(grid, row, col, radius=1):
    """Gets the surrounding pixels of a 2x2 square in a grid."""
    rows, cols = grid.shape
    min_row = max(0, row - radius)
    max_row = min(rows, row + 2 + radius)  # +2 because it's a 2x2 square
    min_col = max(0, col - radius)
    max_col = min(cols, col + 2 + radius)  # +2 because it's a 2x2 square
    return grid[min_row:max_row, min_col:max_col]

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find all 2x2 gray squares
    squares = find_2x2_gray_squares(output_grid)

    # Check surroundings and transform conditionally
    for row, col in squares:
        surrounding1 = get_surrounding_pixels(output_grid, row, col, 1)
        surrounding2 = get_surrounding_pixels(output_grid, row, col, 2)
        
        # Check if all surrounding pixels are black (0)
        if np.all(surrounding1 == 0) and np.all(surrounding2 == 0):
            # Exclude the 2x2 gray square itself from the "all 0" check for surrounding2
            temp_surrounding2 = surrounding2.copy()
            temp_surrounding2[row - (row-1) : row - (row-1) + 2, col-(col-1) : col-(col-1)+2] = 0
            if np.all(temp_surrounding2 == 0):
               output_grid[row:row+2, col:col+2] = 2

    return output_grid