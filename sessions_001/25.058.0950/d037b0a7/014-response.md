# d037b0a7 • 014 • example_2 • investigate_coder

---
```python
"""
Copies the non-zero values from the second row of the input grid to the third row, while leaving other rows unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Copies the non-zero values from the second row to the third row of a 3x3 grid.
    """
    output_grid = np.copy(input_grid)  # Create a copy to avoid modifying the original

    # Iterate through the columns of the second row
    for col in range(output_grid.shape[1]):
        # Copy the value from the second row to the third row if it's non-zero
        if output_grid[1, col] != 0:
            output_grid[2, col] = output_grid[1, col]
        # else zero is maintained

    return output_grid
```

