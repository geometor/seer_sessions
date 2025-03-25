"""
Identify and retain only the unique columns from the input grid, preserving their original order of appearance, to form the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by retaining only unique columns, preserving original order.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Initialize an empty list to store the unique columns
    unique_columns = []

    # Iterate through the columns of the input grid
    for i in range(input_grid.shape[1]):
        current_column = tuple(input_grid[:, i])  # Convert to tuple for easy comparison

        # Check if the current column is already in the unique_columns list
        if current_column not in unique_columns:
            unique_columns.append(current_column)

    # Convert the list of unique columns back into a 2D numpy array
    output_grid = np.column_stack(unique_columns) if unique_columns else np.array([])

    return output_grid.tolist()