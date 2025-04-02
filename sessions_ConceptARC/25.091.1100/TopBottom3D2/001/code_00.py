import numpy as np
from collections import Counter

"""
Transforms the input grid based on the following rule:
1. Identify all unique columns in the input grid by comparing their vertical pixel sequences.
2. Select the leftmost unique column (the one with the smallest column index). If no unique columns exist, return the input grid unchanged.
3. Iterate through each row of the input grid.
4. For each row, check if it contains the background color white (0) and at most one other non-white color. (i.e., the set of unique colors in the row is {0} or {0, C} for some C > 0).
5. If a row satisfies this condition, change the color of the pixel located at the intersection of this row and the selected unique column to white (0) in the output grid.
6. All other pixels retain their original color from the input grid.
"""

def find_unique_columns(grid):
    """
    Identifies indices of columns that are unique in the grid based on their pixel values.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A sorted list of indices of the unique columns. Returns an empty list
              if no columns are unique.
    """
    num_rows, num_cols = grid.shape
    if num_cols <= 1: # A grid with 0 or 1 column has no non-unique columns to compare against
        return list(range(num_cols)) # Or arguably [] if definition requires comparison

    column_tuples = {}
    # Store each column as a tuple and map it to the list of indices where it appears
    for c in range(num_cols):
        # Extract column c as a tuple of its pixel values
        column_data = tuple(grid[:, c])
        # Add the index 'c' to the list associated with this column pattern
        if column_data not in column_tuples:
            column_tuples[column_data] = []
        column_tuples[column_data].append(c)

    unique_column_indices = []
    # Collect indices of columns whose pattern appears exactly once
    for col_data, indices in column_tuples.items():
        if len(indices) == 1:
            unique_column_indices.append(indices[0])

    # Return the indices sorted, maintaining the left-to-right order
    return sorted(unique_column_indices)

def check_row_condition(row):
    """
    Checks if a row contains the background color white (0)
    and at most one other non-white color.

    Args:
        row (np.ndarray): A 1D numpy array representing a row of the grid.

    Returns:
        bool: True if the condition is met, False otherwise.
    """
    # Find all unique color values present in the row
    unique_colors = np.unique(row)

    # Condition 1: The row must contain the background color white (0).
    contains_white = 0 in unique_colors

    # Condition 2: The row must contain at most two unique colors in total.
    # Since we already require white (0) to be present, this means the row can
    # either contain only white ({0}) or white and one other color ({0, C}).
    at_most_two_colors = len(unique_colors) <= 2

    # The row meets the condition only if both sub-conditions are true.
    return contains_white and at_most_two_colors

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)
    num_rows, num_cols = input_grid_np.shape

    # Step 1: Identify all unique columns
    unique_cols_indices = find_unique_columns(input_grid_np)

    # Step 2: Select the leftmost unique column. If none exist, return original grid.
    if not unique_cols_indices:
        # No unique columns found, return the input grid unchanged
        return input_grid_np.tolist()

    # The target column is the unique column with the smallest index
    target_column_index = unique_cols_indices[0]

    # Initialize the output grid as a copy of the input grid. Modifications will be made to this copy.
    output_grid_np = input_grid_np.copy()

    # Step 3 & 4 & 5: Iterate through each row, check condition, and modify output grid if needed
    for r in range(num_rows):
        # Get the current row from the original input grid
        row = input_grid_np[r, :]

        # Check if the current row meets the specified color composition condition
        if check_row_condition(row):
            # If the condition is met, change the pixel in the output grid
            # at this row 'r' and the target column 'target_column_index' to white (0).
            output_grid_np[r, target_column_index] = 0
            # Note: Pixels in rows that don't meet the condition, or pixels outside
            # the target column, remain unchanged due to starting with a copy.

    # Step 6: Return the modified grid, converted back to list of lists format.
    return output_grid_np.tolist()