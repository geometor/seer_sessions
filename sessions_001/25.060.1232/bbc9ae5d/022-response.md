# bbc9ae5d • 022 • example_4 • investigate_coder

---
```python
"""
The transformation rule can be described as follows:
1. Replicate the first four azure (8) pixels vertically to create three rows.
2. Replicate the two white (0) pixels. Add an azure pixel below the last azure.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid based on the input grid's dimensions.
    # The output grid will be 3x6.
    input_height, input_width = input_grid.shape
    output_grid = np.zeros((3, input_width), dtype=int)

    # Replicate the first four azure pixels vertically.
    for i in range(4):
        output_grid[0:3, i] = input_grid[0, i]

    # Copy first white down once
    output_grid[0,4] = input_grid[0,4]

    # Place two last azure and last white
    output_grid[0,5] = input_grid[0,5]
    output_grid[1,5] = input_grid[0,5]
    output_grid[2,4] = input_grid[0,3]


    return output_grid
```
