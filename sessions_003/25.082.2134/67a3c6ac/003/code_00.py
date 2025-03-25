"""
The transformation reorders the columns of the input grid. The columns are sorted
based on a 'sort key' derived from their elements. The exact nature of the sort
key is still under investigation, but it's more complex than just the last
element.  The original relative order of columns with identical sort keys is
preserved.
"""

import numpy as np

def calculate_sort_key(column):
    """
    Calculates a sort key for a given column.  This is a placeholder for the
    actual logic, which needs to be determined. For now, we use a combination
    of the sum of elements and the last element to try and capture some
    column-wise comparison.
    """
    return (sum(column), column[-1])

def transform(input_grid):
    """
    Transforms the input grid by reordering its columns based on a calculated
    sort key.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Get the number of columns.
    num_cols = input_array.shape[1]

    # Create a list of (sort_key, column_index, column_data) tuples.
    column_data = []
    for i in range(num_cols):
        column = input_array[:, i]
        sort_key = calculate_sort_key(column)
        column_data.append((sort_key, i, column))

    # Sort the columns based on the sort key, preserving original order for ties.
    sorted_columns = sorted(column_data, key=lambda x: x[0])

    # Create the output array by assembling the sorted columns.
    output_array = np.empty_like(input_array)
    for i, (_, _, column) in enumerate(sorted_columns):
        output_array[:, i] = column

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()
    return output_grid