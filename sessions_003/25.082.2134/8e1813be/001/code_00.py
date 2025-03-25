"""
Extracts specific rows of uniform color from the input grid and stacks them to create the output grid.
"""

import numpy as np

def is_uniform(row):
    # Check if all elements in the row are the same.
    return np.all(row == row[0])

def transform(input_grid):
    # Initialize an empty list to hold the selected rows.
    selected_rows = []

    # Iterate through each row of the input grid.
    for row in input_grid:
        # Check if the row is uniform and not all zeros (black).
        if is_uniform(row) and row[0] != 0:
            # Add the row to the list of selected rows.
            selected_rows.append(row)

    # Convert the list of selected rows into a NumPy array.
    # If no rows were selected, return an empty array of shape (0,0)
    if not selected_rows:
        return np.array([]).reshape(0, 0)
    
    first_row_len = len(selected_rows[0])
    uniform_selected_rows = [row for row in selected_rows if len(row) == first_row_len]

    output_grid = np.array(uniform_selected_rows)
    
    if output_grid.size == 0:
      return np.array([]).reshape(0,0)

    return output_grid