"""
1. Identify Unique Rows: Examine the input grid and identify all unique rows.
2. Determine Output Type:
    *   If there is only *one* unique row in the input, output the *entire* unique row.
    *   If there are *multiple* unique rows in the input, output a new row containing only the *first element* of each unique row.
3. Construct Output: Create the output grid by, for each unique row according to the rule in step 2.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = []

    # Convert input_grid to numpy array for easier processing
    input_grid = np.array(input_grid)

    # Identify unique rows
    unique_rows = np.unique(input_grid, axis=0)

    # Determine output type and construct output
    if len(unique_rows) == 1:
        # Output the entire unique row
        output_grid.append(unique_rows[0].tolist())  # Convert back to list
    else:
        # Output the first element of each unique row
        for row in unique_rows:
            output_grid.append([row[0]])

    return output_grid