# f2829549 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation extracts all pixels of value '1' (blue) that are in the fourth column.

The new grid has the same amount of rows as the input. It also has width of 3.

Replace the selected blue pixels in the input grid with green pixels (value `3`) in the output.
Maintain the row but set the new column based on this:

- If the blue pixel is located at an even-numbered row index (0-indexed), place the green pixel at column index 0 of the corresponding row in the output grid.
- If the blue pixel is located at an odd-numbered row index, place the green pixel at column index 2 of the corresponding row in the output grid.
- all other output cells are white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with the same number of rows as the input and 3 columns, filled with 0 (white).
    rows = input_grid.shape[0]
    output_grid = np.zeros((rows, 3), dtype=int)

    # Iterate through the input grid to find the blue pixels (value 1) in the fourth column (index 3).
    for i in range(rows):
        if input_grid[i, 3] == 1:
            # If a blue pixel is found, determine the output column based on row index parity.
            output_col = 0 if i % 2 == 0 else 2
            # Set the corresponding pixel in the output grid to green (value 3).
            output_grid[i, output_col] = 3

    return output_grid
```
