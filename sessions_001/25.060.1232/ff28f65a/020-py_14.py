"""
1.  **Input:** A 2D grid of colored pixels.
2.  **Output:** A 3x3 grid of colored pixels, where each cell is either white (0) or blue (1).
3.  **Process:**
    *   Identify all 2x2 contiguous blocks of red (2) pixels in the input grid.
    *   Conceptually divide the input grid into nine regions. The boundaries of these regions are determined by dividing the input grid's height and width by 3.  These regions may overlap.
    *   For each cell in the 3x3 output grid:
        *   Determine the corresponding region in the input grid.
        *   Check if *any part* of a 2x2 red square intersects with that region. It's sufficient for even a single pixel of the red square to fall within the region.
        *   If *any part* of a 2x2 red square intersects with the region, set the corresponding output cell to blue (1).
        *   Otherwise, set the output cell to white (0).
"""

import numpy as np

def find_squares(grid, size, color):
    """Finds all contiguous blocks of a specified size and color."""
    squares = []
    for i in range(grid.shape[0] - size + 1):
        for j in range(grid.shape[1] - size + 1):
            if np.all(grid[i:i+size, j:j+size] == color):
                squares.append((i, j))
    return squares

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)
    # Find all 2x2 red squares
    red_squares = find_squares(input_grid, 2, 2)

    height, width = input_grid.shape
    row_step = height / 3.0
    col_step = width / 3.0

    for i in range(3):
        for j in range(3):
            # Define the boundaries of the current region
            row_start = int(i * row_step)
            row_end = int((i + 1) * row_step)
            col_start = int(j * col_step)
            col_end = int((j + 1) * col_step)

            # Check for any red squares intersecting with this region
            for r_sq_row, r_sq_col in red_squares:
                # Check for overlap.  We check if any of the four corners of the
                # 2x2 square are within the region.
                if (row_start <= r_sq_row < row_end and col_start <= r_sq_col < col_end) or \
                   (row_start <= r_sq_row + 1 < row_end and col_start <= r_sq_col < col_end) or \
                   (row_start <= r_sq_row < row_end and col_start <= r_sq_col + 1 < col_end) or \
                   (row_start <= r_sq_row + 1 < row_end and col_start <= r_sq_col + 1 < col_end):
                    output_grid[i, j] = 1
                    break  # Once an intersection is found, move to the next output cell

    return output_grid