# 178fcbfb • 002 • example_3 • investigate_coder

---
```python
"""
Transforms an input grid by replicating the red (2) pixels vertically and 
replicating the other non zero pixels horizontally.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # 1. & 2. Vertical Replication of Red Pixels
    for row_index, row in enumerate(input_grid):
        for col_index, pixel in enumerate(row):
            if pixel == 2:
                output_grid[:, col_index] = 2

    # 3. & 4. Horizontal replication of other colored pixels
    for row_index, row in enumerate(input_grid):
        for col_index, pixel in enumerate(row):
            if pixel != 0 and pixel != 2:
                output_grid[row_index, :] = pixel
    
    return output_grid.tolist()
```
