# b190f7f5 • 004 • example_1 • investigate_coder

---
```python
"""
Expands each non-zero pixel in the input grid into a 3x3 block of the same color in the output grid, preserving relative positioning. Zero pixels remain as zero filled 3x3.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the expansion rule.
    """
    input_grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows * 3, cols * 3), dtype=int)  # Initialize output grid

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            pixel_value = input_grid[r, c]
            
            # Calculate top-left coordinates of the 3x3 block in output grid
            output_row_start = r * 3
            output_col_start = c * 3

            # Expand non-zero pixels to 3x3 blocks
            if pixel_value != 0:
                output_grid[output_row_start:output_row_start+3, output_col_start:output_col_start+3] = pixel_value
            # Zero expansion to 3x3 is done by default because output grid is initialized with zeros.

    return output_grid.tolist() # convert back
```
