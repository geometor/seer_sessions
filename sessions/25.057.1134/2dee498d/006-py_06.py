"""
The transformation extracts specific columns from the input grid to create the output grid. The number of rows remains the same. The columns to be selected change based on the input. The selection does not follow a strict "every third column" rule. It appears the selected column indexes are: 0, 3, 6, and 9 for input grid widths of 11 and 12. With width 13, the column indexes are 0, 2, 4, 8, and 10.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    
    if cols == 11 or cols == 12:
        selected_columns = [0, 3, 6, 9]
    elif cols == 13:
        selected_columns = [0, 2, 4, 8, 10]
    else:
        selected_columns = [] # handle cases not covered

    output_grid = np.zeros((rows, len(selected_columns)), dtype=int)
    
    # change output pixels
    for i, col_index in enumerate(selected_columns):
        if col_index < cols:  # Ensure index is within bounds
           output_grid[:, i] = input_grid[:, col_index]

    return output_grid.tolist()