```python
"""
The output grid is formed by taking only the rows and columns with at least one non-zero element from the input grid, re-arranging and moving all non-zero pixels to fill a new rectangular grid, starting at the top-left corner (0,0). Pixels of color 5 are removed.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by compacting non-zero pixels (excluding 5s)
    to the top-left corner, removing empty rows and columns.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    input_array = np.array(input_grid)

    # 1. Identify Non-Zero Rows and Columns
    rows_with_non_zero = np.any(input_array != 0, axis=1)
    cols_with_non_zero = np.any(input_array != 0, axis=0)

    # 2. Create a new grid (determine dimensions)
    num_rows = np.sum(rows_with_non_zero)
    num_cols = np.sum(cols_with_non_zero)
    output_grid = np.zeros((num_rows, num_cols), dtype=int)
    
    #3. populate the output, excluding 0 and 5
    output_row = 0
    output_col = 0
    
    for i in range(input_array.shape[0]):
        if not rows_with_non_zero[i]:
            continue
        for j in range(input_array.shape[1]):
            if not cols_with_non_zero[j]:
                continue
            
            if input_array[i,j] != 0 and input_array[i,j] != 5:
                output_grid[output_row, output_col] = input_array[i,j]
                output_col += 1
                if output_col >= num_cols:
                    output_col = 0
                    output_row += 1

    return output_grid.tolist()
```