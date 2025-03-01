# d23f8c26 • 002 • example_3 • investigate_coder

---
```python
"""
Extract the third column (index 2) from the input grid and set all other values in the output grid to 0.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting the third column and setting all other values to 0.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.zeros_like(input_grid)

    # Extract the third column (index 2).
    selected_column = input_grid[:, 2]

    # Set the third column of the output grid to the selected column.
    output_grid[:, 2] = selected_column

    return output_grid
```
