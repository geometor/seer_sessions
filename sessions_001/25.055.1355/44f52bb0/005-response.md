# 44f52bb0 • 005 • refine_coder

---
```python
"""
1. Count Red Pixels: Count the number of red pixels (value `2`) in the input grid.
2. Create Output Grid: Create a new output grid consisting of a single column.
3. Populate with Grey: The height of the output grid (number of rows) is equal to the count of red pixels in the input grid.  All pixels in this grid are grey (value `5`).
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    # Count red pixels in the input grid
    input_array = np.array(input_grid)
    red_count = np.count_nonzero(input_array == 2)

    # Create an output grid with a single column and height equal to red_count
    output_grid = np.full((red_count, 1), 5)

    return output_grid.tolist()
```
