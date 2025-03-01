# c3e719e8 • 016 • refine_coder

---
```python
"""
The input grid is replicated four times in a 2x2 tiling pattern to create the output grid. The output grid's dimensions are twice the input grid's dimensions in both height and width. The four copies of the input grid completely fill the output grid.
"""

import numpy as np

def transform(input_grid):
    # Determine Output Size: The output grid's dimensions are twice the input grid's dimensions.
    input_height, input_width = input_grid.shape
    output_height = input_height * 2
    output_width = input_width * 2

    # Create Output Grid: Initialize an output grid filled with zeros.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place Replicas: Position the four copies within the output grid in a 2x2 arrangement.
    # Top-Left
    output_grid[:input_height, :input_width] = input_grid
    # Top-Right
    output_grid[:input_height, input_width:input_width * 2] = input_grid
    # Bottom-Left
    output_grid[input_height:input_height * 2, :input_width] = input_grid
    # Bottom-Right
    output_grid[input_height:input_height * 2, input_width:input_width * 2] = input_grid

    return output_grid
```

