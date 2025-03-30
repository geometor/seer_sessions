import numpy as np
import itertools

"""
Identify all 2x2 azure (8) squares in the input grid.
For every pair of these squares, check if they are horizontally or vertically aligned.
If horizontally aligned (sharing the same two rows), check if the entire 2-row high path strictly between them consists only of white (0) pixels. If it does, fill that entire path with orange (7).
If vertically aligned (sharing the same two columns), check if the entire 2-column wide path strictly between them consists only of white (0) pixels. If it does, fill that entire path with orange (7).
The original azure squares and any other pre-existing non-white colored squares remain unchanged.
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
    # Iterate up to height-2 and width-2 to allow for 2x2 check
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
    Transforms the input grid by filling regions between aligned 2x2 azure squares
    only if the entire path between them is white.

    Args:
        input_grid (np.array): The 2D numpy array representing the input grid.

    Returns:
        np.array: The transformed 2D numpy array.
    """
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    azure_color = 8
    fill_color = 7
    background_color = 0

    # 1. Identify all 2x2 azure squares
    azure_squares = find_2x2_squares(output_grid, azure_color)

    # 2. Iterate through all unique pairs of identified azure squares
    for (r1, c1), (r2, c2) in itertools.combinations(azure_squares, 2):
        # 3a. Check for horizontal alignment (same rows)
        if r1 == r2:
            # Determine left and right squares
            left_c = min(c1, c2)
            right_c = max(c1, c2)
            
            # Check if path is clear
            path_is_clear = True
            # Iterate columns from the right edge of the left square + 1
            # up to (but not including) the left edge of the right square.
            for c_check in range(left_c + 2, right_c):
                # Check if the cells in the path are NOT white
                if (output_grid[r1, c_check] != background_color or
                    output_grid[r1 + 1, c_check] != background_color):
                    path_is_clear = False
                    break # Found an obstacle, stop checking this path
            
            # If the entire path was clear, fill it
            if path_is_clear:
                for c_fill in range(left_c + 2, right_c):
                    output_grid[r1, c_fill] = fill_color
                    output_grid[r1 + 1, c_fill] = fill_color

        # 3c. Check for vertical alignment (same columns)
        elif c1 == c2:
            # Determine top and bottom squares
            top_r = min(r1, r2)
            bottom_r = max(r1, r2)

            # Check if path is clear
            path_is_clear = True
            # Iterate rows from the bottom edge of the top square + 1
            # up to (but not including) the top edge of the bottom square.
            for r_check in range(top_r + 2, bottom_r):
                 # Check if the cells in the path are NOT white
                 if (output_grid[r_check, c1] != background_color or
                     output_grid[r_check, c1 + 1] != background_color):
                     path_is_clear = False
                     break # Found an obstacle, stop checking this path

            # If the entire path was clear, fill it
            if path_is_clear:
                for r_fill in range(top_r + 2, bottom_r):
                     output_grid[r_fill, c1] = fill_color
                     output_grid[r_fill, c1 + 1] = fill_color

    # 4. Return the modified output grid
    return output_grid