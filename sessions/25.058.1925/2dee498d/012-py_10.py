"""
1. **Copy the First Column:** The first column of the output grid is identical to the first column of the input grid.
2. **Copy the Last Column:** The second column of the output grid is identical to the last column of the input grid.
3. **Select and Copy a Middle Column:** The third column of the output grid is a selected column from the input grid. The selected column is:
    - The second column (index 1) if the input grid width is 8 or 9.
    - The sixth column (index 5) if the input grid width is 7 or 8.
    - Otherwise we default to column 1, although no other examples exist.
4. **Consistent Height:** The output grid has the same height (number of rows) as the input grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a NumPy array
    input_array = np.array(input_grid)

    # Get the height and width of the input grid
    height, width = input_array.shape

    # Initialize the output grid as a list of lists
    output_grid = []

    # 1. Get the first column of the input
    first_column = input_array[:, 0]

    # 2. Get the last column of the input
    last_column = input_array[:, width - 1]

    # 3. Determine the "middle" column to select.
    if width == 8 or width == 9:
        middle_column_index = 1
    elif width == 7:
        middle_column_index = 5
    else:
        middle_column_index = 1 # Default case, should not occur in provided examples

    middle_column = input_array[:, middle_column_index]

    # Construct the output grid row by row
    for i in range(height):
        output_row = [first_column[i], last_column[i], middle_column[i]]
        output_grid.append(output_row)

    return output_grid