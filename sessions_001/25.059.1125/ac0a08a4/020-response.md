# ac0a08a4 • 020 • refine_coder

---
```python
"""
Expands a 3x3 input grid into a 15x15 output grid. Non-zero pixels in the input
are expanded into 5x5 blocks of the same color in the output. Zero pixels are
handled differently:  The 5x5 output blocks corresponding to input zero-pixels
take the colors from the expansions of the non-zero pixels in the same row and
column.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 15x15 output grid filled with zeros.
    output_grid = np.zeros((15, 15), dtype=int)

    # Iterate through each pixel of the 3x3 input grid.
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            pixel_value = input_grid[i, j]

            # Determine the top-left corner of the 5x5 block.
            row_start = i * 5
            col_start = j * 5

            if pixel_value != 0:
                # Fill the 5x5 block with the value of the input pixel.
                output_grid[row_start:row_start + 5, col_start:col_start + 5] = pixel_value
            else:
                # Zero Pixel Handling: combine expansions from the same row and column
                # First, expand non-zero pixels in the same row.
                for col in range(input_grid.shape[1]):
                    if input_grid[i, col] != 0:
                        output_grid[row_start:row_start + 5, col * 5:col * 5 + 5] = input_grid[i, col]
                # Then, expand non-zero pixels in the same column.
                for row in range(input_grid.shape[0]):
                    if input_grid[row, j] != 0:
                       output_grid[row * 5:row * 5 + 5, col_start:col_start + 5] = input_grid[row, j]

    return output_grid
```

