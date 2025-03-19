"""
1. **Identify Non-White Rows:** Examine each row of the input grid.
2. **Filter Rows:** Select only the rows that have at least one pixel that is not white (value 0).
3. **Construct Output:** Create the output grid by vertically stacking the selected rows, preserving their original order. The result is a new grid containing only the non-white rows from the input.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array
    grid = np.array(input_grid)
    
    # Initialize an empty list to hold the non-white rows
    output_rows = []

    # Iterate through each row of the grid
    for row in grid:
        # Check if the row contains any non-white pixels (non-zero values)
        if np.any(row != 0):
            # Add the row to the output_rows list
            output_rows.append(row)

    # Convert the list of rows to a NumPy array
    output_grid = np.array(output_rows)

    return output_grid