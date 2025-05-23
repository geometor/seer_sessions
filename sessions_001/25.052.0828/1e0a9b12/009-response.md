# 3-1e0a9b12 • 009 • example_3 - NLP

---
Okay, let's analyze the transformation from the input grid to the output grid.

**YAML Description of Observations**

```yaml
task: 009-example_3
observations:
  input_grid:
    size: 5x5
    objects:
      - color: 1 (blue)
        positions: [(0, 3), (2, 3)]
      - color: 3 (green)
        positions: [(1, 1), (2, 1), (4, 1)]
      - color: 2 (red)
        positions: [(2, 4)]
      - color: 6 (magenta)
        positions: [(3, 0)]
  output_grid:
    size: 5x5
    objects:
      - color: 1 (blue)
        positions: [(3, 3), (4, 3)]
      - color: 3 (green)
        positions: [(2, 1), (3, 1), (4, 1)]
      - color: 2 (red)
        positions: [(4, 4)]
      - color: 6 (magenta)
        positions: [(4, 0)]
```

**Natural Language Program**

Here's a step-by-step description of the transformation:

1.  **Identify Objects:** Locate all colored cells (non-zero) in the input grid. The objects here are individual single colored cells.

2.  **Move Down:** Each colored object of the grid moves down.

3. **Bottom Row Priority:** If any colored cells are in the last row, they persist in their positions.

4.  **Stack:** If by moving down, two or more objects coincide, the object originally positioned lower takes the place.

**Transformation Rule Summary**

The transformation involves moving down all the colored cells to the bottom row.

```python
"""
The transformation involves moving all colored cells down to the bottom row, maintaining their original column positions. If a cell is already in the bottom row, it remains unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by moving all non-zero colored cells to the bottom row,
    while keeping cells already on the bottom row unchanged.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each column
    for j in range(cols):
        # Find non-zero elements in the column
        non_zero_indices = np.nonzero(input_grid[:, j])[0]
        if non_zero_indices.size > 0:
          # Check what is at the bottom
          colored_cell = input_grid[non_zero_indices[-1],j]
          output_grid[rows-1,j]=colored_cell
          
    # Copy elements already at the bottom to the output grid
    for i in range(cols):
      if input_grid[rows-1,i]!=0:
        output_grid[rows-1,i]=input_grid[rows-1,i]

    return output_grid
```

