```python
"""
Transforms a 3x3 input grid containing 0s and 5s into a 3x3 output grid.
The color of a '5' in the input is determined by its row position and the position of other 5's.
'0' values in the input are replaced by a single color based on a row-mapping of 5's.
"""

import numpy as np

def _get_color_for_row(input_grid, row_index):
    """Helper function to determine the color based on row index and 5's positions."""
    rows, cols = input_grid.shape
    fives_positions = np.where(input_grid == 5)
    all_fives_in_last_column = all(fives_positions[1] == cols - 1)
    any_five_in_first_column = any(fives_positions[1] == 0)
    any_five_in_first_or_second_column = any(np.isin(fives_positions[1],[0,1]))

    if row_index == 0:
        if all_fives_in_last_column:
            return 3  # Green
        elif any_five_in_first_column:
            return 2 # Red
        else:
            return 4
    elif row_index == 1:
        if any_five_in_first_or_second_column:
            return 4  # Yellow
        else:
            return 3 # Green
    elif row_index == 2:
        if all_fives_in_last_column:
            return 4 # Yellow
        else:
           return 2  # Red
    return 0 # Should not happen

def transform(input_grid):
    # Initialize output_grid with the same dimensions and type as the input.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Determine colors for each row based on '5' positions.
    row_colors = [_get_color_for_row(input_grid, r) for r in range(rows)]

    # Fill the output grid row by row
    for r in range(rows):
      output_grid[r,:] = row_colors[r]
    
    return output_grid
```