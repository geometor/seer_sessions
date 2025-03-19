# 49d1d64f • 020 • refine_coder

---
```python
"""
The transformation rule can be described as follows:

1.  **Create a new grid:** Create a new grid that is larger than the input grid by one row and one column on *each side* (top, bottom, left, and right). This means the new grid's dimensions will be (input_rows + 2, input_cols + 2).
2.  **Fill with zeros:** Initialize all cells of the new grid with the value 0 (black).
3. **Embed Input:** Copy the input grid onto the new, larger grid. The top-left corner of the input grid should be placed at position (1, 1) in the new grid. This will leave a border of 0s (black pixels) one pixel wide around the original input grid.
"""

import numpy as np

def transform(input_grid):
    # Determine the dimensions of the input grid.
    input_rows, input_cols = input_grid.shape

    # Calculate the dimensions of the output grid.
    output_rows = input_rows + 2
    output_cols = input_cols + 2

    # Create the output grid, filled with black pixels (color 0).
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Copy the input grid to the correct position within the output grid.
    for i in range(input_rows):
        for j in range(input_cols):
            output_grid[i + 1, j + 1] = input_grid[i, j]

    return output_grid
```

