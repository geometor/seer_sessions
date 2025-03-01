# 017c7c7b • 012 • refine_coder

---
```python
"""
Expands the input grid vertically by a factor of 1.5, substituting blue (1) pixels with red (2) pixels, and preserving white (0) pixels in their corresponding expanded positions.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid. The output grid width is the same as the input,
    # and height is 1.5 times the input height.
    input_height, input_width = input_grid.shape
    output_height = int(input_height * 1.5)
    output_width = input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the input grid and map values to the output.
    for r in range(input_height):
        for c in range(input_width):
            output_row = int(r * 1.5) # Calculate the potential output row.

            # Check for a valid output_row index by making sure that the 
            # multiplication has no fractional component.
            if (r * 1.5) == output_row:
                if input_grid[r, c] == 1:  # If blue
                    output_grid[output_row, c] = 2  # Change to red
                elif input_grid[r,c] == 0: # if white
                    output_grid[output_row, c] = input_grid[r, c]  # Copy white pixels

    return output_grid
```

