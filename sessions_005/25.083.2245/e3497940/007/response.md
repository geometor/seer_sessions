```python
"""
1.  **Iterate through each row** of the input grid.
2.  **Locate the first Gray (5) pixel** in the current row. This pixel acts as the dividing point.
3.  **Extract Pixels:** Copy all pixels to the left of the located Gray pixel in the current row, creating the `left_object`.
4.  **Mirror:** Horizontally flip the `left_object`.
5.  **Construct Output Grid:** The output grid will have the same number of rows as the input grid. The number of output columns is the same as the column index of the gray pixel.
6.  **Output:** Return the flipped pixels as the new grid.
"""

import numpy as np

def find_first_gray_column(row):
    """Finds the column index of the first gray pixel in a row."""
    try:
        return np.where(row == 5)[0][0]
    except IndexError:
        return -1  # No gray pixel found

def transform(input_grid):
    """Transforms the input grid by extracting the region to the left of the first gray pixel in each row and mirroring it."""
    num_rows = input_grid.shape[0]
    
    # Find the gray marker column for each row.
    gray_marker_cols = [find_first_gray_column(row) for row in input_grid]

    # Determine number of columns in the output by using maximum of gray bar
    # columns
    num_cols = max(gray_marker_cols)    
    if num_cols < 0:      
        return np.zeros((num_rows, 0), dtype=int)   
    # Initialize the output grid
    output_grid = np.zeros((num_rows, num_cols), dtype=int)

    # Iterate through each row, extract, mirror, and copy pixels
    for i, row in enumerate(input_grid):
        gray_col = gray_marker_cols[i]
        if gray_col > 0:  # Only copy if a gray pixel was found
            left_object = row[:gray_col]
            mirrored_object = np.flip(left_object)
            output_grid[i, :gray_col] = mirrored_object

    return output_grid
```
