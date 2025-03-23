"""
For each row in the input grid, extract the distinct values, preserving their original order. Construct the output grid by stacking these extracted rows vertically.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting unique values in order from each row.
    """
    output_grid = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Find distinct values in the current row, preserving order
        distinct_values = []
        for value in row:
            if value not in distinct_values:
                distinct_values.append(value)

        # Append the distinct values as a new row in the output grid
        output_grid.append(distinct_values)

    # Convert the list of lists to a NumPy array.  Handle cases where rows have varying lengths
    max_len = max(len(row) for row in output_grid) if output_grid else 0
    
    # Pad shorter rows
    padded_output_grid = []
    for row in output_grid:
        if(len(row) < max_len):
          padding = [0] * (max_len - len(row))
          padded_row = row + padding
          padded_output_grid.append(padded_row)
        else:
          padded_output_grid.append(row)


    return np.array(padded_output_grid)