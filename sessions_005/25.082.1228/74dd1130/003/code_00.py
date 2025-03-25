"""
Sorts the elements within each column of a 3x3 grid independently,
based on the global frequency of each color in the input grid. Colors
with higher global frequency appear first. If colors have the same frequency,
they are sorted in ascending order.
"""

import numpy as np

def global_frequencies(grid):
    """Calculates the global frequencies of each color in the grid."""
    grid = np.array(grid)
    unique, counts = np.unique(grid, return_counts=True)
    return dict(zip(unique, counts))

def transform(input_grid):
    """
    Sorts each column of the input grid based on global color frequencies.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A 3x3 list of lists representing the output grid, with each column sorted.
    """
    # Calculate global frequencies.
    freqs = global_frequencies(input_grid)

    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Initialize an empty output array.
    output_array = np.empty_like(input_array)

    # Iterate over each column.
    for j in range(input_array.shape[1]):
        # Get the current column.
        column = input_array[:, j]

        # Sort the column based on global frequency and then value.
        sorted_column = sorted(column, key=lambda x: (-freqs[x], x))

        # Assign the sorted column to the output array.
        output_array[:, j] = sorted_column

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid