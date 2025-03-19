"""
1.  **Locate the 2x2 Green Square:** Find the top-left corner coordinates of the 2x2 green square. This serves as the reference point.

2.  **Extend Blue Pixels:**
    *   If a blue pixel is in a row *strictly above* the top row of the green square, transform the four pixels to its right to blue (if they exist within the grid boundaries).
    *   If a blue pixel is in a row *strictly below* the top row of the green square, transform the pixel to its right to blue (if it exists within grid boundaries).

3.  **Move/Remove Magenta Pixels:**
    *   If a magenta pixel is in a row *strictly above* the top row of the green square *and* in a column *strictly to the right* of the leftmost column of the green square, move it down one row (if the new position is within the grid boundaries), and clear the original position.
    *   If a magenta pixel is in a row *strictly above* the top row of the green square and is in the same column or *to the left* of the green square's leftmost column, remove the magenta pixel (change its value to 0).
    *    If a magenta pixel is in the *same row* as the *top* of the green square, do *not* move or change the pixel.
"""

import numpy as np

def find_objects(grid, color):
    """Finds the coordinates of all pixels of a given color."""
    return np.argwhere(grid == color).tolist()

def find_square(grid, color):
    """Finds a 2x2 square of the specified color and returns its top-left corner coordinates."""
    rows, cols = grid.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            if (grid[i, j] == color and grid[i + 1, j] == color and
                grid[i, j + 1] == color and grid[i + 1, j + 1] == color):
                return (i, j)  # Top-left corner
    return None

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = np.copy(input_grid)

    # 1. Locate the 2x2 Green Square
    green_square_coords = find_square(input_grid, 3)
    if green_square_coords is None:
        return output_grid  # Return original if no green square
    green_top_row = green_square_coords[0]
    green_left_col = green_square_coords[1]


    # 2. Extend Blue Pixels
    blue_pixels = find_objects(input_grid, 1)
    for row, col in blue_pixels:
        if row < green_top_row:  # Strictly above
            for i in range(1, 5):  # Extend four pixels to the right
                if col + i < output_grid.shape[1]:
                    output_grid[row, col + i] = 1
        elif row > green_top_row:  # Strictly below
            if col + 1 < output_grid.shape[1]:
                output_grid[row, col + 1] = 1

    # 3. Move/Remove Magenta Pixels
    magenta_pixels = find_objects(input_grid, 6)
    for row, col in magenta_pixels:
        if row < green_top_row: # Strictly above green square top row
            if col > green_left_col:  # Strictly to the right
                if row + 1 < output_grid.shape[0]:
                    output_grid[row + 1, col] = 6
                    output_grid[row, col] = 0
            else:  # Same column or to the left
                output_grid[row, col] = 0
        # else: same row as top of green square, do nothing.

    return output_grid