"""
1.  **Initialization:** Create an output grid identical to the input grid.
2.  **Pixel Iteration:** Iterate through each pixel of the input grid, row by row and column by column.
3.  **White Preservation:** If the current pixel value is '0' (white), keep its value unchanged in the output grid.
4.  **Azure Transformation:** If the current pixel value is '8' (azure):
    *   Determine the starting color for the alternating sequence based on whether the row index is even or odd. If row is even, start the alternation with 2. if the row is odd start with 5.
    *   If the row index is even, and it's the first '8' encountered in this row, replace it with '2' (red); the next 8 with 5, then 2 and so on.
    *    If the row index is odd, and it's the first '8' encountered in this row, replace it with '5' (gray), then with 2, then 5, and so on.
5.  **Output:** Return the modified output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for i in range(rows):
        eight_count = 0  # Counter for '8's in the current row
        for j in range(cols):
            # Preserve '0'
            if input_grid[i, j] == 0:
                continue  # Do nothing, keep '0' as is
            # Conditional Substitution for '8'
            elif input_grid[i, j] == 8:
                # Determine starting color based on row parity
                if i % 2 == 0:  # Even row
                    if eight_count % 2 == 0:
                        output_grid[i, j] = 2  # Red
                    else:
                        output_grid[i, j] = 5  # Gray
                else:  # Odd row
                    if eight_count % 2 == 0:
                        output_grid[i, j] = 5  # Gray
                    else:
                        output_grid[i, j] = 2  # Red
                eight_count += 1  # Increment the '8' counter

    return output_grid