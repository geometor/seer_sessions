```python
"""
The transformation extracts all pixels that are not 0 or 5 from the input grid.
The relative position of the non-zero and non-5 values in each row and column of the input are preserved in the output grid.
The output grid is always 3x3, and zeros are used as padding.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting non-zero, non-5 pixels
    and arranging them sequentially into a 3x3 output grid, preserving
    relative positions and padding with zeros.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed 3x3 grid.
    """
    input_array = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)
    rows, cols = input_array.shape

    # Collect non-zero and non-5 pixels with their original coordinates
    valid_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_array[r, c] != 0 and input_array[r, c] != 5:
                valid_pixels.append((input_array[r, c], r, c))

    # Determine the relative positions for the output grid.  This is the tricky
    # part and will likely need further refinement based on more examples.
    #  We are essentially creating a mapping from input coordinates to output
    #  coordinates.

    if valid_pixels:
      # find bounds of input pixels
        min_row = min(p[1] for p in valid_pixels)
        min_col = min(p[2] for p in valid_pixels)
        max_row = max(p[1] for p in valid_pixels)
        max_col = max(p[2] for p in valid_pixels)

        row_scale = 1.0
        col_scale = 1.0

        if max_row > min_row:
            row_scale = 2.0 / (max_row - min_row)
        if max_col > min_col:
            col_scale = 2.0 / (max_col - min_col )

        for (value, r, c) in valid_pixels:
            out_r = int(round((r - min_row) * row_scale))
            out_c = int(round((c-min_col) * col_scale))

            if 0 <= out_r < 3 and 0 <= out_c < 3:
                output_grid[out_r,out_c] = value



    return output_grid.tolist()
```