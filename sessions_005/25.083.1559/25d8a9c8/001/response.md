```python
"""
Iterates through each row of the input grid. If all pixels in a row are the same, the corresponding output row is all 5s (gray). Otherwise, the output row is all 0s (white).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid to a 3x3 output grid based on row-wise pixel equality.
    """
    output_grid = np.zeros_like(input_grid)  # Initialize output grid with the same dimensions and type

    # Iterate through each row
    for i in range(input_grid.shape[0]):
        row = input_grid[i, :]
        # Check if all pixels in the row are the same
        if np.all(row == row[0]):
            # If all pixels are the same, set the corresponding output row to 5
            output_grid[i, :] = 5
        else:
            # Otherwise, set the corresponding output row to 0
            output_grid[i, :] = 0

    return output_grid
```