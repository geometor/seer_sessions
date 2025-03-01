# cce03e0d • 018 • refine_coder

---
```python
"""
The input grid is replicated once, creating two copies of the original. These copies are then placed adjacent to each other, either horizontally, vertically or diagonally to form a larger grid. The output grid's dimensions are double of input grid for width and height, meaning the output grid always have four instances of original input pixels.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Calculate output grid dimensions
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize output_grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Embed the input grid four times to form a 2x2 pattern
    output_grid[0:input_height, 0:input_width] = input_grid
    output_grid[0:input_height, input_width:output_width] = input_grid
    output_grid[input_height:output_height, 0:input_width] = input_grid
    output_grid[input_height:output_height, input_width:output_width] = input_grid
    
    return output_grid
```
