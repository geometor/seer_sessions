"""
1.  **Check Input Dimensions:** Examine the dimensions of the input grid.

2.  **Handle 1xN and Nx1 Inputs:** If the input grid has only one row *or* one column, the output is a 1x1 grid.
    *   Find the middle element of the input grid. The output grid's single cell will have the value of that input element.

3.  **Handle Other Inputs (>= 2x2):** If the input grid has more than one row and more than one column:
    *   Divide the input grid into four quadrants: top-left, top-right, bottom-left, and bottom-right. If the grid has an odd number of rows or columns, the "middle" row/column is included in both the top/bottom and left/right quadrants, respectively.
    *   Create a 2x2 output grid.
    *   For each quadrant:
        *   Find the *first* non-white (non-zero) color in the quadrant when iterating by row, then by column.
        *   Set the corresponding cell in the 2x2 output grid to the color found:
            *   Top-left quadrant color -> output[0, 0]
            *   Top-right quadrant color -> output[0, 1]
            *   Bottom-left quadrant color -> output[1, 0]
            *   Bottom-right quadrant color -> output[1, 1]
        *   If a quadrant contains *only* white pixels, the corresponding cell in the output grid remains 0 (white).
"""

import numpy as np

def get_first_non_white_color(grid, quadrant):
    """
    Finds the first non-white color in a quadrant of the grid.

    Args:
        grid: The input numpy array.
        quadrant: A tuple (row_start, row_end, col_start, col_end) defining the quadrant.

    Returns:
        The first non-white color (integer) found, or 0 if only white is present.
    """
    row_start, row_end, col_start, col_end = quadrant
    subgrid = grid[row_start:row_end, col_start:col_end]
    for row in subgrid:
        for pixel in row:
            if pixel != 0:
                return pixel  # Return the first non-white color
    return 0  # Return 0 (white) if no non-white color is found

def transform(input_grid):
    rows, cols = input_grid.shape

    # Handle 1xN and Nx1 inputs
    if rows == 1 or cols == 1:
        # Find the middle element
        if rows == 1:
            middle_index = cols // 2
            output_grid = np.array([[input_grid[0, middle_index]]])
        else:  # cols == 1
            middle_index = rows // 2
            output_grid = np.array([[input_grid[middle_index, 0]]])
        return output_grid

    # Handle >= 2x2 inputs
    else:
        # Initialize output_grid
        output_grid = np.zeros((2, 2), dtype=int)

        # Define quadrants
        mid_row = rows // 2
        mid_col = cols // 2
        quadrants = {
            "top_left": (0, mid_row, 0, mid_col),
            "top_right": (0, mid_row, mid_col, cols),
            "bottom_left": (mid_row, rows, 0, mid_col),
            "bottom_right": (mid_row, rows, mid_col, cols),
        }

        # Change output pixels based on quadrant colors
        output_grid[0, 0] = get_first_non_white_color(input_grid, quadrants["top_left"])
        output_grid[0, 1] = get_first_non_white_color(input_grid, quadrants["top_right"])
        output_grid[1, 0] = get_first_non_white_color(input_grid, quadrants["bottom_left"])
        output_grid[1, 1] = get_first_non_white_color(input_grid, quadrants["bottom_right"])

        return output_grid