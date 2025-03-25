"""
The transformation reorders the columns of the input grid. The columns are sorted 
in ascending order based on the value of their last element. If two columns have 
the same last element, their original relative order is preserved.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reordering its columns based on the last element.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Get the number of columns.
    num_cols = input_array.shape[1]

    # Create a list of (last_element, column_index, column_data) tuples.
    column_data = []
    for i in range(num_cols):
        column = input_array[:, i]
        last_element = column[-1]
        column_data.append((last_element, i, column))

    # Sort the columns based on the last element, preserving original order for ties.
    sorted_columns = sorted(column_data, key=lambda x: x[0])

    # Create the output array by assembling the sorted columns.
    output_array = np.empty_like(input_array)
    for i, (_, _, column) in enumerate(sorted_columns):
        output_array[:, i] = column

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()
    return output_grid