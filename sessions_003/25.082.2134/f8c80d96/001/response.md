```python
"""
Replaces '0' (white) pixels in the input grid with '5' (gray) pixels based on the presence of non-zero pixels to their left. If a non-zero pixel is found to the left within the same row, the '0' is replaced by the value of the closest non-zero pixel to its left; otherwise, it's replaced by '5'.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the defined rule.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # If the current cell is not '0', copy it to the output grid
            if input_grid[r, c] != 0:
                output_grid[r, c] = input_grid[r, c]
            else:
                # Find the closest non-zero pixel to the left
                replacement_value = 5
                for c_left in range(c - 1, -1, -1):  # Iterate backwards from c-1 to 0
                    if input_grid[r, c_left] != 0:
                        replacement_value = input_grid[r, c_left]
                        break  # Stop once the first non-zero pixel is found
                
                output_grid[r, c] = replacement_value

    return output_grid
```