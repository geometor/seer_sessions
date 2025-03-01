# 91413438 • 020 • example_4 • investigate_coder

---
```python
"""
The 3x3 input grid is replicated six times horizontally and two times vertically in the top-left corner of an 18x18 output grid. The rest of the output grid is filled with zeros.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as an 18x18 array filled with zeros.
    output_grid = np.zeros((18, 18), dtype=int)

    # Get the dimensions of the input grid.
    input_height, input_width = input_grid.shape

    # Replicate the input grid six times horizontally and two times vertically
    for i in range(2):
        for j in range(6):
            output_grid[i*input_height:(i+1)*input_height, j*input_width:(j+1)*input_width] = input_grid

    return output_grid
```
