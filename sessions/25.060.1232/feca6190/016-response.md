# feca6190 • 016 • example_3 • investigate_coder

---
```python
"""
The input is a 1x5 grid (a row of pixels). The output is a 15x15 grid.
The input row is replicated diagonally in the output grid, starting from the bottom-left corner and moving up and to the right.
The remaining pixels in the output grid are filled with black (0).
"""

import numpy as np

def transform(input_grid):
    # Get the input row.
    input_row = input_grid[0]

    # Determine the size of the output grid.
    n = len(input_row) * input_grid.shape[1]
    output_size = len(input_row) * input_grid.shape[0]


    # Create the output grid filled with 0s.
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # Replicate the input row diagonally.
    for i in range(output_size):
        for j, color in enumerate(input_row):
            if i - (output_size-1) + j >= 0 and i - (output_size -1) + j < output_size:
                output_grid[i - (output_size-1) + j, i] = color
    return output_grid
```
