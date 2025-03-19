"""
1.  **Identify the Target Column:** Find the single column in the input grid that contains the color orange.
2.  **Verify Column Consistency:** Ensure all other pixels (non-orange) within the identified column are the same color.
3.  **Replicate the Column:** Create four copies of this entire column.
4. **Assemble Output:** Place the four copied columns next to one another.  All other columns in the input grid are discarded. The output grid consists *only* of the four replicated columns.
"""

import numpy as np

def get_target_column(grid):
    # Find the column index containing orange (color 7).
    orange_col_indices = np.where(np.any(grid == 7, axis=0))[0]
    if len(orange_col_indices) > 0:
        return orange_col_indices[0]  # Return the first occurrence
    else:
        return None

def is_column_consistent(grid, col_index):
    # Check if all non-orange pixels in the column have the same color.
    column = grid[:, col_index]
    non_orange_pixels = column[column != 7]
    if len(non_orange_pixels) > 0:
        return np.all(non_orange_pixels == non_orange_pixels[0])
    else:
        return True  # Consider a column with only orange as consistent

def replicate_column(column, count):
    # Replicate a column 'count' times.
    return np.tile(column, (count, 1)).T

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    target_col_index = get_target_column(input_grid)
    
    if target_col_index is None:  # No orange found
        return input_grid # should not happen, based on problem
    
    if not is_column_consistent(input_grid, target_col_index):
        return input_grid # should not happen, based on observations

    # Extract the target column
    target_column = input_grid[:, target_col_index]

    # Replicate the target column four times
    replicated_columns = replicate_column(target_column, 4)
    output_grid = replicated_columns

    return output_grid