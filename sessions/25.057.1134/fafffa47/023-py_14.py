"""
1.  **Input Reduction:** The input grid (6x3) is vertically halved to produce a 3x3 output grid.

2.  **Maroon Detection:** Identify all cells in the input grid containing the color maroon (9).

3.  **Red Placement Rule:**
    *   If a maroon (9) pixel is found on the *second* row of the input, a red (2) pixel is placed in the *first* row of the output, in the *same* column.
    *   If a maroon (9) pixel is found on the *fourth* row of the input, a red (2) pixel is placed in the *second* row of the output, in the *same* column.

4.  **No Maroon, No Red:** If no maroon pixels are found in the input, the output grid remains all black (or the background color, 0).
5. Blue is ignored.
"""

import numpy as np

def transform(input_grid):
    """Transforms an input grid according to the ARC task rules."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)  # Initialize 3x3 output

    # Iterate through the input grid, checking rows 2 and 4 for maroon (9)
    for col in range(input_grid.shape[1]):
        if input_grid[1, col] == 9:  # Second row (index 1)
            output_grid[0, col] = 2  # Place red in first row (index 0)
        if input_grid[3, col] == 9:  # Fourth row (index 3)
            output_grid[1, col] = 2  # Place red in second row (index 1)

    return output_grid