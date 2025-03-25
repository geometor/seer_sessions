```python
"""
The transformation rule works as follows:
1. Identify Non-Empty Rows: Examine each row in the input grid. A row is considered "non-empty" if it contains any digit other than 0.
2. Shift Non-Empty Rows Upwards: Arrange all non-empty rows sequentially at the top of the output grid, maintaining their relative order from the input.
3. Fill Remaining with empty rows: insert empty (all 0) rows to bottom of the grid until the input and output grid have the same height.
"""

import numpy as np

def is_empty_row(row):
    """Checks if a row is empty (all zeros)."""
    return all(pixel == 0 for pixel in row)

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape
    output_grid = []

    # Identify and shift non-empty rows
    non_empty_rows = []
    for row in input_grid_np:
        if not is_empty_row(row):
            non_empty_rows.append(list(row))

    # Add non-empty rows to output
    for row in non_empty_rows:
        output_grid.append(row)

    # Pad with empty rows at top and bottom
    num_empty_rows = rows - len(output_grid)
    
    while len(output_grid) < rows :
       output_grid.append([0] * cols)

    return output_grid
```