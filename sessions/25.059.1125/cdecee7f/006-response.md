# cdecee7f • 006 • refine_coder

---
```python
"""
Transforms a 10x10 grid by finding the non-zero pixel in the fifth row and placing it in the top-left corner of a 3x3 output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a 3x3 array filled with zeros
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the non-zero pixel in the fifth row (index 4)
    for col_index, pixel_value in enumerate(input_grid[4]):
        if pixel_value != 0:
            # Place the non-zero pixel in the top-left corner of the output grid
            output_grid[0][0] = pixel_value
            break  # Exit the loop after finding the first non-zero pixel

    return output_grid
```
