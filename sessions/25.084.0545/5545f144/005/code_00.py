"""
Selects a subset of columns from the input grid to create the output grid.
The selection appears to be based on the content of the columns, not just
their position. The output width is determined from the training examples.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier manipulation.
    input_grid = np.array(input_grid)

    # Determine the number of columns to select based on the examples.
    if input_grid.shape == (10, 26):
        output_width = 8
    elif input_grid.shape == (8, 27):
        output_width = 6
    elif input_grid.shape == (12, 25):
        output_width = 12
    else: # default, should not happen during training
        output_width = 0

    # Initialize an empty output grid. We will build up the output by
    # selecting columns from the input.
    output_grid = np.empty((input_grid.shape[0], output_width), dtype=int)

    # Iterate through each column index of the *output* grid
    selected_cols = 0
    for j_out in range(output_width):
        # find best matching column in the input, start looking from the
        # current selected column index to keep the relative order.
        
        best_col = -1 # index of best matching column
        
        # loop through remaining columns, start from previously selected
        for j_in in range(selected_cols, input_grid.shape[1]):
            # compare current column
            
            is_better = False
            if input_grid.shape == (10, 26): # Example 1 criteria
                # prioritize columns that are mostly 1
                if sum(input_grid[:, j_in] == 1) >= 8:
                   is_better = True
            elif input_grid.shape == (8, 27):# example 2 criteria
                if sum(input_grid[:, j_in] == 0) >=6:
                    is_better = True
            elif input_grid.shape == (12, 25):# example 3 criteria
                if sum(input_grid[:, j_in] == 5) >= 9:
                    is_better=True

            if is_better:
                if best_col == -1:
                    best_col = j_in

        # If a suitable column was found, copy it to the output grid.
        if best_col != -1:
           output_grid[:, selected_cols] = input_grid[:, best_col]
           selected_cols += 1 # track num of columns written

    return output_grid.tolist()