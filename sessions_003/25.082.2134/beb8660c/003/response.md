```python
"""
Transforms the input grid by identifying rows with non-black pixels ("data rows"), stacking them at the bottom of the output grid, and cyclically shifting non-black pixel values within certain columns to the left. Remaining rows at the top are filled with black pixels.
"""

import numpy as np

def _is_data_row(row):
    """Checks if a row contains at least one non-black pixel."""
    return np.any(row != 0)

def _get_data_rows(grid):
    """Extracts and returns data rows and their original indices."""
    data_rows = []
    indices = []
    for i, row in enumerate(grid):
        if _is_data_row(row):
            data_rows.append(row)
            indices.append(i)
    return data_rows, indices

def _shift_column_values(grid):
    """Cyclically shifts non-black values in each column to the left."""
    grid = np.array(grid)
    rows, cols = grid.shape
    shifted_grid = np.copy(grid)

    for j in range(cols):
        column_values = grid[:, j]
        non_black_indices = np.where(column_values != 0)[0]
        non_black_values = column_values[non_black_indices]

        if len(non_black_values) > 0:  # Check if there are non-black values
          shifted_non_black_values = np.roll(non_black_values, -1)
          shifted_grid[non_black_indices, j] = shifted_non_black_values
    return shifted_grid

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Get data rows and their original indices
    data_rows, _ = _get_data_rows(input_grid)

    # Calculate the starting row index for placing data rows at the bottom
    num_data_rows = len(data_rows)
    start_row = rows - num_data_rows

    # Place data rows at the bottom of the output grid
    for i, row in enumerate(data_rows):
        output_grid[start_row + i, :] = row
    
    # Apply cyclic shift to the non-black values in columns
    output_grid = _shift_column_values(output_grid)


    return output_grid.tolist()
```