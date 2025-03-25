```python
"""
The output grid's height is the same as the input grid's height. The output
grid's width is double the input grid's width. The input grid is copied
directly to the left half of the output grid. The right half of the output
grid is an exact copy of the left half.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Calculate output grid dimensions
    output_height = input_height
    output_width = input_width * 2

    # Initialize the output grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy the input grid to the left half of the output grid
    output_grid[:, :input_width] = input_grid

    # Copy the left half (original input) to the right half
    output_grid[:, input_width:] = input_grid

    return output_grid
```