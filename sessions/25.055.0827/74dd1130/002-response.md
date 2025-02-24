# 74dd1130 • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule is a clockwise rotation of the grid by 90 degrees. The cell at (row, col) in the input grid moves to (col, 2 - row) in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise.
    """
    # Convert the input list of lists to a NumPy array
    input_array = np.array(input_grid)

    # Initialize the output grid with the same dimensions as the input
    rows, cols = input_array.shape
    output_grid = np.zeros_like(input_array)
    
    # Iterate through the cells of input grid to perform rotation
    for i in range(rows):
      for j in range(cols):
        output_grid[j, rows - 1 - i] = input_array[i,j]

    return output_grid.tolist()
```
