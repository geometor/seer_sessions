"""
The transformation extracts every third column from the input grid, starting with the first, to create the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting every third column, starting from the first.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid with selected columns.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Get the number of columns in the input grid.
    num_cols = input_array.shape[1]

    # Create a list to store the indices of the columns to be selected.
    selected_cols = []

    # Iterate through the column indices, selecting every third column starting from 0.
    for i in range(0, num_cols, 3):
        selected_cols.append(i)

    # Use NumPy's column indexing to extract the selected columns.
    output_array = input_array[:, selected_cols]

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid