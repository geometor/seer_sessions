# 44f52bb0 • 002 • example_1 • investigate_coder

---
```python
"""
Counts the number of red (value '2') pixels in the input grid.
If the count is 4, the output is a 1x1 grid with a blue (1) pixel.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Count the number of red (2) pixels.
    red_count = np.count_nonzero(input_array == 2)

    # Create the output grid based on the count.
    if red_count == 4:
        output_grid = [[1]]  # 1x1 grid with a blue pixel
    else:
        output_grid = [[0]] # added for generalization

    return output_grid
```
