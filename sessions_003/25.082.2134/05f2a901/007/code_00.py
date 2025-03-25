"""
1.  **Identify Non-White Rows:** Determine all rows in the input grid that contain at least one pixel that is not white (color 0).
2.  **Count Non-White Rows:** Count the total number of rows identified in step 1.
3. **Center the Block:**
    *   Calculate the starting row index for the block of non-white rows. This is done by subtracting the number of non-white rows from the total number of rows in the grid and dividing the result by two. Use integer division (floor). `start_row = (rows - num_non_white_rows) // 2`
4.  **Stack Rows:** Copy the identified non-white rows from the input grid to the output grid, starting at the calculated `start_row` index. Maintain the original relative order of the non-white rows.
5. **Preserve Empty Rows:** All other rows in the output grid should be all white (all pixels set to 0).
6. **Preserve Shape:** the contents of the non-white input rows are exactly the same as the output rows.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by identifying non-white rows,
    and centering them in the output grid.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # 1. Identify Non-White Rows and 2. Count Non-White Rows
    non_white_row_indices = []
    for r in range(rows):
        if not np.all(input_grid[r] == 0):  # More efficient check for non-white rows
            non_white_row_indices.append(r)
    num_non_white_rows = len(non_white_row_indices)

    # 3. Center the Block
    start_row = (rows - num_non_white_rows) // 2

    # 4. Stack Rows
    current_output_row = start_row
    for r in non_white_row_indices:
        output_grid[current_output_row] = input_grid[r]
        current_output_row += 1

    # 5. Preserve Empty Rows (already handled by initializing with zeros)
    # 6. preserve shape (already handled)

    return output_grid.tolist()