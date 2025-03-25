```python
"""
The transformation involves conditionally mirroring segments of rows in a grid. The condition for mirroring
is based on whether the two central columns of a row contain any non-zero values. If they do, the two
cells to the left and right of the central columns are mirrored; otherwise, the row remains unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule of conditional row segment mirroring.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify the two center columns
    center_col1 = cols // 2 - 1
    center_col2 = cols // 2

    # Iterate through each row
    for i in range(rows):
        # Conditional Mirroring Check: Check if the two central columns contain any non-zero values.
        if input_grid[i, center_col1] != 0 or input_grid[i, center_col2] != 0:
            # Mirroring:
            #   Identify the segment of two cells to the left of the two central columns.
            left_segment = input_grid[i, center_col1-2:center_col1]
            #   Identify the segment of two cells to the right of the two central columns.
            right_segment = input_grid[i, center_col2+1:center_col2+3]
            
            #   Mirror segments
            if center_col1 - 2 >= 0:
                output_grid[i, center_col1-2:center_col1] = right_segment[::-1]  # reverse
            if center_col2 + 3 <= cols:
                output_grid[i, center_col2+1:center_col2+3] = left_segment[::-1]  #reverse

        # Row Preservation: If the central columns contain only zeros, the row is already copied.
    return output_grid
```