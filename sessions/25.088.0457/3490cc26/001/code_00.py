import numpy as np
import itertools

"""
Identify all 2x2 azure (8) squares in the input grid. 
For every pair of these squares, check if they are horizontally or vertically aligned.
If horizontally aligned (sharing the same two rows), fill the rectangular region strictly between them (in the same rows) with orange (7).
If vertically aligned (sharing the same two columns), fill the rectangular region strictly between them (in the same columns) with orange (7).
The original azure squares and any other colored squares (like red, 2) remain unchanged.
"""

def find_2x2_squares(grid, color):
    """
    Finds the top-left coordinates of all 2x2 squares of a specific color.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to search for.

    Returns:
        list: A list of tuples (row, col) representing the top-left coordinates.
    """
    squares = []
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(width - 1):
            # Check if the 2x2 block starting at (r, c) matches the color
            if (grid[r, c] == color and
                grid[r+1, c] == color and
                grid[r, c+1] == color and
                grid[r+1, c+1] == color):
                squares.append((r, c))
    return squares

def transform(input_grid):
    """
    Transforms the input grid by filling regions between aligned 2x2 azure squares.

    Args:
        input_grid (np.array): The 2D numpy array representing the input grid.

    Returns:
        np.array: The transformed 2D numpy array.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    azure_color = 8
    fill_color = 7

    # 1. Identify all 2x2 azure squares
    azure_squares = find_2x2_squares(output_grid, azure_color)

    # 2. Iterate through all unique pairs of identified azure squares
    for (r1, c1), (r2, c2) in itertools.combinations(azure_squares, 2):
        # 3a. Check for horizontal alignment (same rows)
        if r1 == r2:
            # Determine left and right squares
            left_c = min(c1, c2)
            right_c = max(c1, c2)
            # 3b. Fill the region strictly between them
            # Rows are r1 and r1 + 1
            # Columns are from left_c + 2 up to (but not including) right_c
            if right_c > left_c + 2: # Ensure there's space between them
                output_grid[r1:r1+2, left_c+2:right_c] = fill_color

        # 3c. Check for vertical alignment (same columns)
        elif c1 == c2:
            # Determine top and bottom squares
            top_r = min(r1, r2)
            bottom_r = max(r1, r2)
            # 3d. Fill the region strictly between them
            # Columns are c1 and c1 + 1
            # Rows are from top_r + 2 up to (but not including) bottom_r
            if bottom_r > top_r + 2: # Ensure there's space between them
                 output_grid[top_r+2:bottom_r, c1:c1+2] = fill_color

    # 4. Return the modified output grid
    return output_grid