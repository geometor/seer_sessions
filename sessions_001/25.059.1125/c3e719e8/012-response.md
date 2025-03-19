# c3e719e8 • 012 • example_2 • investigate_coder

---
```python
"""
The input grid is replicated four times in a 2x2 pattern within a larger 9x9 output grid. The remaining cells of the output grid are filled with 0s.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 9x9 output grid with zeros
    output_grid = np.zeros((9, 9), dtype=int)

    # Get the dimensions of the input grid
    input_height, input_width = input_grid.shape

    # Copy the input grid to the top-left corner
    output_grid[:input_height, :input_width] = input_grid

    # Copy the input grid to the top-right corner
    output_grid[:input_height, 6:9] = input_grid

    # Copy the input grid to the bottom-left corner
    output_grid[6:9, :input_width] = input_grid
    
    # Copy the input grid to the bottom-right corner
    output_grid[6:9, 6:9] = input_grid

    return output_grid
```
