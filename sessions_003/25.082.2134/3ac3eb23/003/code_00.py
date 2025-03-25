"""
1.  **Copy:** Iterate through all pixels in the input grid. Copy any non-black pixel to the output grid at the same position.

2.  **Shadow Generation (Top Row Only):** For each non-black pixel *in the top row* of the input grid:

    *   Create a "shadow" by repeating a 2x2 diagonal extending every two rows downwards and one column to the left:
    * calculate the number of shadow repetitions by dividing the number of
      rows by 2
    *    For each repetition:
        *   Add a pixel of the same color one row below the origin, one column to the left.
        *   Add a pixel of the same color one row below the origin, at the original column.

3.  **Output:** The output grid consists of the original non-black pixels plus the generated shadows.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    input_np = np.array(input_grid)
    output_np = np.copy(input_np)
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
                row_offset += 1
                if row_offset < rows:
                    # Pixel to the left
                    if c - 1 >= 0:
                        output_np[row_offset, c-1] = color
                    # pixel at the same column
                    output_np[row_offset, c] = color

    return output_np.tolist()