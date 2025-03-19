"""
The transformation extracts columns from the input grid, sorts them based on the number of unique colors within each column (most unique to least), and then places these sorted columns into an output grid of the same dimensions as the input.
"""

import numpy as np

def get_columns(grid):
    """
    Splits a grid into columns.
    """
    columns = []
    for i in range(grid.shape[1]):
        columns.append(grid[:, i])
    return columns

def count_unique_colors(column):
    """
    Counts the number of unique colors in a column.
    """
    return len(np.unique(column))

def sort_columns_by_unique_colors(columns):
    """
    Sorts columns based on the count of unique colors, descending.
    """
    return sorted(columns, key=count_unique_colors, reverse=True)

def transform(input_grid):
    """
    Transforms the input grid according to the described rules.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Extract columns from the input grid.
    columns = get_columns(input_grid)

    # Sort columns by the number of unique colors.
    sorted_columns = sort_columns_by_unique_colors(columns)

    # Create an output grid with the same dimensions as the input.
    output_grid = np.zeros_like(input_grid)

    # Place the sorted columns into the output grid.
    for j, col in enumerate(sorted_columns):
        output_grid[:, j] = col

    return output_grid.tolist()