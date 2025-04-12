"""
The transformation rule is to crop the input grid by removing the first row and the first column.
The output grid consists of the subgrid starting from the second row and second column of the input grid.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Removes the first row and the first column from the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid, which is a subgrid
        of the input grid.
    """
    # Convert the input list of lists to a NumPy array for easier slicing
    input_array = np.array(input_grid, dtype=int)

    # Check if the grid has at least 2 rows and 2 columns to crop
    if input_array.shape[0] < 2 or input_array.shape[1] < 2:
        # Handle edge case: if the grid is too small to crop,
        # return an empty grid or handle as per specific requirements.
        # Here, returning an empty list of lists.
        return []

    # Select all rows starting from the second row (index 1)
    # Select all columns starting from the second column (index 1)
    output_array = input_array[1:, 1:]

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
