"""
The transformation rule filters rows from the input grid based on the first element of each row. Rows starting with 0 or 5 are removed. The remaining rows are included in the output grid *as they are*, without modification and preserving their original order.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by selecting rows that do not start with 0 or 5, preserving original row content."""

    # Convert input_grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)

    # Initialize an empty list to store the selected rows
    selected_rows = []

    # Iterate through each row of the input array
    for row in input_array:
        # Check if the first element of the row is not 0 and not 5
        if row[0] != 0 and row[0] != 5:
            # If the condition is met, append the *entire* row to the selected_rows list
            selected_rows.append(row)

    # Convert the list of selected rows to a NumPy array
    output_array = np.array(selected_rows)

    return output_array.tolist()