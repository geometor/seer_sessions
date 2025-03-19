# 7b7f7511 • 016 • example_3 • investigate_coder

---
```python
"""
The input grid is transformed into the output grid by reducing its height. The output grid consists of the top half of the input grid.

Specifically, the program takes rows from the input grid at indices 0, 1, and 2, and then constructs the entire output grid from them.
"""

import numpy as np

def transform(input_grid):
    """Transforms an input grid by taking the top half of it."""
    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Calculate the number of rows in the output grid (half the input rows).
    output_rows = rows // 2

    # Initialize the output grid with the correct dimensions.
    output_grid = np.empty((output_rows, cols), dtype=int)

    # Copy the top half of the input grid to the output grid.
    output_grid = input_grid[:output_rows, :]
    
    return output_grid
```
