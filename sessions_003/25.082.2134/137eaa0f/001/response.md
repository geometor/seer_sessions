```python
"""
Extracts all rows from the input that contain any colored objects, removes
the background (zero) pixels, and keeps only colored pixels on each row to
construct the output grid. The output grid's rows are ordered to match the
order of non-empty rows in the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting non-zero pixels from rows
    containing non-zero elements, preserving their order.
    """
    output_rows = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Extract non-zero pixels from the current row
        non_zero_pixels = [pixel for pixel in row if pixel != 0]

        # If there are any non-zero pixels, append them to the output rows
        if non_zero_pixels:
            output_rows.append(non_zero_pixels)

    # Convert the list of rows to a NumPy array (output grid)
    output_grid = np.array(output_rows)

    return output_grid
```