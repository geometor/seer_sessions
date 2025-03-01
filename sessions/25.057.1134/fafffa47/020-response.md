# fafffa47 • 020 • example_4 • investigate_coder

---
```python
"""
Divide the input grid (6x3) into nine 2x1 regions. Consider them as cells of a 3x3 grid.
The order of the 2x1 blocks are read from left to right, top to bottom. The first 2x1 block is the top left block, etc.
Inspect each of these 2x1 regions:
    *   If any of them contains a maroon (9) pixel, and zero blue (1), output a red (2) pixel in the corresponding position of the output grid.
    *   If not, output a white (0) pixel in the corresponding position of the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 6x3 input grid into a 3x3 output grid based on the presence of maroon (9)
    and the absence of blue(1) in 2x1 regions of the input.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)  # Initialize output grid with white (0)

    for row in range(3):
        for col in range(3):
            # Define the 2x1 region in the input grid
            region = input_grid[row * 2:row * 2 + 2, col]

            # Check for the presence of maroon (9) and absence of blue (1) in the region.
            if 9 in region and 1 not in region:
                output_grid[row, col] = 2  # Set corresponding output pixel to red (2)
            else:
                output_grid[row, col] = 0  # Set corresponding output pixel to white (0)
    
    return output_grid.tolist()
```
