"""
1.  **Copy:** Copy all non-black pixels from the input grid to the output grid, maintaining their original positions.

2.  **Shadow Generation (Top Row):** For each non-black pixel in the *top row* of the input grid:
    * Determine the pixel's color.
    * Calculate the number of shadow repetitions by integer dividing the number of rows in the grid by 2.
     - Start one row below and one col to the left
        *   Create a shadow pixel of the same color.
     - Move to the cell to the right
        * create a shadow pixel of the same color
    *   Repeat for the number of repetitions, starting the next block 2 rows down from the previous block.

3.  **Output:** The output grid is the combination of copied non-black pixels and the generated shadow pixels.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    input_np = np.array(input_grid)
    output_np = np.zeros_like(input_np)
    rows, cols = input_np.shape

    # Copy non-black pixels
    for r in range(rows):
        for c in range(cols):
            if input_np[r, c] != 0:
                output_np[r, c] = input_np[r, c]

    # Shadow Generation (Top Row Only)
    for c in range(cols):
        if input_np[0, c] != 0:
            color = input_np[0, c]
            num_repetitions = rows // 2
            for i in range(num_repetitions):
                row_offset = 1 + i * 2
                if row_offset < rows:
                    # Pixel to the left
                    if c - 1 >= 0:
                        output_np[row_offset, c - 1] = color
                    # Pixel at the same column
                    output_np[row_offset, c] = color


    return output_np.tolist()