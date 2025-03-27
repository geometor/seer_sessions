```python
"""
The transformation rule identifies a "center" region in the input grid defined by non-zero values and creates reflections of this center shape. These reflections are placed around the original center shape, creating a larger output grid.
"""

import numpy as np

def get_center_row_indices(grid):
    """Finds row indices with non-zero elements."""
    rows = []
    for i, row in enumerate(grid):
        if any(val != 0 for val in row):
            rows.append(i)
    return rows

def get_center_col_indices(grid):
    """Finds column indices with non-zero elements."""
    cols = []
    for j in range(len(grid[0])):
        if any(grid[i][j] != 0 for i in range(len(grid))):
            cols.append(j)
    return cols

def reflect_shape(shape_grid):
    """Reflects shape of grid both horiz/vert"""
    h_reflected = np.flip(shape_grid, axis=1)
    v_reflected = np.flip(shape_grid, axis=0)
    hv_reflected = np.flip(v_reflected, axis=1)

    reflected_grid = np.zeros((shape_grid.shape[0] * 2 -1, shape_grid.shape[1] * 2 -1))
    
    # place original
    for i in range(shape_grid.shape[0]):
        for j in range(shape_grid.shape[1]):
            reflected_grid[i + shape_grid.shape[0] -1 -i][j + shape_grid.shape[1]-1-j] = shape_grid[i][j]

    # insert horizontal reflection
    for i in range(h_reflected.shape[0]):
         for j in range(h_reflected.shape[1]):
            reflected_grid[i + h_reflected.shape[0] - 1- i][j + shape_grid.shape[1]]= h_reflected[i][j]
            
    # insert vertical reflection 
    for i in range(v_reflected.shape[0]):
         for j in range(v_reflected.shape[1]):
            reflected_grid[i + shape_grid.shape[0]][j + v_reflected.shape[1] -1 - j]= v_reflected[i][j]


    # insert corner reflection
    for i in range(hv_reflected.shape[0]):
        for j in range(hv_reflected.shape[1]):
            reflected_grid[i + shape_grid.shape[0]][j + shape_grid.shape[1]]= hv_reflected[i][j]

    return reflected_grid

def transform(input_grid):
    """Transforms the input grid according to the shape reflection/expansion rule."""
    input_grid = np.array(input_grid)
    center_rows = get_center_row_indices(input_grid)
    center_cols = get_center_col_indices(input_grid)

    if not center_rows or not center_cols:
        return input_grid.tolist()  # Handle edge case of all zeros.


    # use center of non-zero rows/cols
    center_row_start = center_rows[0]
    center_row_end = center_rows[-1] + 1  # inclusive
    center_col_start = center_cols[0]
    center_col_end = center_cols[-1] +1

    center_shape = input_grid[center_row_start:center_row_end, center_col_start:center_col_end]

    # reflect/expand
    reflected_shape = reflect_shape(center_shape)

    
    return reflected_shape.tolist()
```