# 05269061 • 011 • refine_coder

---
```python
"""
The input grid is replicated twice horizontally and twice vertically to form the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replicating it twice horizontally and twice vertically.
    """
    # Get the dimensions of the input grid
    input_height, input_width = input_grid.shape

    # Create an output grid with doubled dimensions
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=input_grid.dtype)

    # Replicate the input grid into the output grid
    for i in range(2):
        for j in range(2):
            output_grid[i * input_height:(i + 1) * input_height, j * input_width:(j + 1) * input_width] = input_grid

    return output_grid
```
