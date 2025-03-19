# feca6190 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule takes a 1x5 input grid and expands it into a 5x5 output grid.
The single non-zero (red) pixel in the input grid becomes a diagonal line of red pixels
in the output grid, stretching from the bottom-left to the top-right.
All other pixels in the output grid are white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize the 5x5 output grid with zeros.
    output_grid = np.zeros((5, 5), dtype=int)

    # Find the non-zero pixel in the input grid.
    non_zero_indices = np.where(input_grid != 0)
    non_zero_value = input_grid[non_zero_indices]

    # Check to handle potential empty input or no non-zero elements.
    if non_zero_indices[0].size > 0 :
          # Create the diagonal line of red pixels in output.
          for i in range(5):
            output_grid[4-i, i] = non_zero_value[0]

    return output_grid
```

