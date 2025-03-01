# d631b094 • 008 • example_2 • investigate_coder

---
```python
"""
Finds all red cells in the input and creates a 1x3 output grid filled with red cells.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to output.
    """
    # Initialize output_grid as a 1x3 numpy array filled with zeros.
    output_grid = np.zeros((1, 3), dtype=int)

    # Find all cells with value 2 in the input grid.
    red_cells = np.where(np.array(input_grid) == 2)

    # Count the number of red cells (though not strictly necessary for this specific task)
    # num_red_cells = len(red_cells[0])

    # If red color exist, Set all cells in output_grid to 2
    if len(red_cells[0]) > 0:
      output_grid[:] = 2

    return output_grid.tolist()
```
