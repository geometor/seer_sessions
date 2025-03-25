```python
"""
The transformation extracts all pixels that are not 0 or 5 from the input grid.
Extracted pixels are arranged sequentially into a smaller 3x3 grid, filling row by row, from top-left.
Rows and columns of the input grid that contain all zeros are not included in the output grid. The output grid
is always 3x3.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting non-zero, non-5 pixels
    and arranging them sequentially into a 3x3 output grid.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed 3x3 grid.
    """
    input_array = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)
    output_row = 0
    output_col = 0

    # Iterate through the input grid in row-major order
    for i in range(input_array.shape[0]):
        for j in range(input_array.shape[1]):
            # Check if the pixel is non-zero and non-5
            if input_array[i, j] != 0 and input_array[i, j] != 5:
                # Place the pixel in the next available position in the output grid
                output_grid[output_row, output_col] = input_array[i, j]
                output_col += 1
                if output_col >= 3:  # Move to the next row if the current row is full
                    output_col = 0
                    output_row += 1
                if output_row >= 3: # stop if output is full
                    break
        if output_row >=3:
            break

    return output_grid.tolist()
```