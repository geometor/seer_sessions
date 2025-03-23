```python
"""
The transformation rule is as follows:

1.  **Copy Input:** Begin with a copy of the input grid.
2.  **Shift First Column:** In the first column of the copied grid, shift all
    values down by one row. The value in the first row of the first column
    remains unchanged.
3. **Add new last column**: Create a new column to the right of the grid, an
    exact copy of the now modified, first column.
4. **Preserve other columns**: Values from the input grid for all columns
    except the first and the new last column remain unchanged
5.  **Return:** The modified grid is the output.
"""

import numpy as np

def transform(input_grid):
    # Copy the input grid to initialize the output grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Shift the first column down by one, keeping the first element the same.
    first_column = output_grid[:, 0].copy()  # Create a copy to avoid modifying the original first column
    for i in range(rows - 1, 0, -1):
        output_grid[i, 0] = first_column[i-1]


    # add new last column
    new_col = output_grid[:, 0].copy()
    output_grid = np.column_stack((output_grid, new_col))

    return output_grid
```