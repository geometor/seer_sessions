```python
"""
Transforms an input grid into an output grid based on the following rules:

1. **First Row Rule:** If the first row of the input grid has only one unique value, the first row of the output is all 5s. Otherwise, it's all 0s.

2. **Subsequent Rows Rule:** For subsequent rows, if any value in the current row is *not* present in the first row, the output row is all 5s. Otherwise (if all values in the current row are also in the first row), the output row is all 0s.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with the same dimensions as the input
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Get unique values in the first row of the input
    first_row_unique_values = set(input_grid[0])

    # Process first row
    if len(first_row_unique_values) == 1:
        output_grid[0, :] = 5
    else:
        output_grid[0, :] = 0

    # Process remaining rows
    for i in range(1, rows):
        # Get unique values in the current row
        current_row_unique_values = set(input_grid[i])

        # Check if the current row contains any value NOT in the first row
        if not current_row_unique_values.issubset(first_row_unique_values):
            output_grid[i, :] = 5
        # else all values are in the first row, so keep 0

    return output_grid
```