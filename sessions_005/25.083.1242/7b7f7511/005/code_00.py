"""
1.  **Identify Unique Columns:** Examine the input grid and identify all unique columns. A column is considered unique if its sequence of values is not identical to any other column.
2.  **Construct Output Columns:** Create the output grid by using the *unique columns* from the input.
3.  **Determine Output Rows**: The output grid should contain the same number of rows as the input, *up to* but not exceeding the number of unique columns. If the input has *more* rows than unique columns, only include a number of rows equal to the number of unique columns.
"""

import numpy as np

def get_unique_columns(grid):
    """Helper function to extract unique columns from a grid."""
    grid_array = np.array(grid)
    unique_cols = []
    seen_cols = []

    for i in range(grid_array.shape[1]):
        col = tuple(grid_array[:, i])  # Convert column to tuple for easy comparison
        if col not in seen_cols:
            unique_cols.append(grid_array[:, i].tolist())
            seen_cols.append(col)
    return unique_cols

def transform(input_grid):
    """
    Transforms the input grid based on the unique columns rule.
    """
    # Get unique columns
    unique_columns = get_unique_columns(input_grid)

    # Determine the number of rows for the output grid
    num_input_rows = len(input_grid)
    num_unique_cols = len(unique_columns)
    num_output_rows = min(num_input_rows, num_unique_cols)

    # Construct the output grid
    output_grid = []
    for i in range(num_output_rows):
        row = []
        for col in unique_columns:
            row.append(col[i])  # Corrected indexing to handle cases where input has more rows
        output_grid.append(row)

    return output_grid