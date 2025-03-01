# ac0a08a4 • 016 • example_3 • investigate_coder

---
```python
"""
Expands each pixel of a 3x3 input grid into a 5x5 block in a 15x15 output grid.
Non-zero pixels in the input are replicated as 5x5 blocks of the same color.
Zero pixels in the input effectively result in skipping the corresponding 5x5 block in the output.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 15x15 output grid filled with zeros.
    output_grid = np.zeros((15, 15), dtype=int)

    # Iterate through each pixel of the 3x3 input grid.
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            # Expansion: For each pixel in the input grid:
            pixel_value = input_grid[i, j]
            
            # if non-zero, set 5x5
            if pixel_value != 0:
                # Determine the top-left corner of the 5x5 block.
                row_start = i * 5
                col_start = j * 5

                # Fill the 5x5 block with the value of the input pixel.
                output_grid[row_start:row_start + 5, col_start:col_start + 5] = pixel_value

    return output_grid
```
