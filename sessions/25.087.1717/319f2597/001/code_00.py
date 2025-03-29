"""
Transformation rule:
1. Identify the first pair of adjacent columns (C, C+1) in the input grid where at least one row contains the value 0 (white) in both column C and column C+1.
2. Create a copy of the input grid as the initial output grid.
3. Iterate through each row R of the grid.
4. If the *input* grid has 0 at (R, C) and 0 at (R, C+1) (a "special row"):
    a. Iterate through all columns 'col' in row R of the *output* grid.
    b. If the corresponding cell in the *input* grid (R, col) is not 2 (red), set the cell in the *output* grid (R, col) to 0 (white). Otherwise, keep the original value (which must be 2).
5. If the row is not a "special row":
    a. Check the cell in the *output* grid at (R, C). If its value is not 2 (red), set it to 0 (white).
    b. Check the cell in the *output* grid at (R, C+1). If its value is not 2 (red), set it to 0 (white).
    c. Leave all other cells in this row of the output grid unchanged (they retain their copied value from the input).
6. Return the modified output grid.
"""

import copy
import numpy as np # numpy is commonly used for grid manipulations

def find_target_columns(grid):
    """
    Finds the index C of the first of two adjacent columns (C, C+1)
    that contain the pattern [0, 0] in at least one row.

    Args:
        grid (list of lists): The input grid.

    Returns:
        int or None: The index C of the first target column, or None if no such pair is found.
    """
    height = len(grid)
    if height == 0:
        return None
    width = len(grid[0])
    if width < 2:
        return None

    for r in range(height):
        for c in range(width - 1):
            if grid[r][c] == 0 and grid[r][c+1] == 0:
                return c  # Return the index of the first column in the pair
    return None # No such pattern found

def transform(input_grid):
    """
    Applies the transformation rule based on identifying special columns
    and processing rows differently based on their content in those columns.

    Args:
        input_grid (list of lists): The input 2D grid of integers.

    Returns:
        list of lists: The transformed 2D grid.
    """
    # Ensure input is handled as a list of lists for consistency
    input_list = [list(row) for row in input_grid]
    height = len(input_list)
    if height == 0:
        return []
    width = len(input_list[0])
    if width == 0:
        return [[] for _ in range(height)]

    # 1. Identify Target Columns
    target_col_c = find_target_columns(input_list)

    # If no target columns are found, return a copy of the input (or handle as error)
    # Based on examples, target columns are always found.
    if target_col_c is None:
        # This case might need specific handling depending on requirements.
        # For now, return a copy, assuming the pattern always exists if modification is needed.
        return copy.deepcopy(input_list)

    target_col_c1 = target_col_c + 1

    # 2. Initialize Output Grid
    output_grid = copy.deepcopy(input_list)

    # 3. Process Each Row
    for r in range(height):
        # 4. Check Row Type (using the original input grid for the check)
        is_special_row = (input_list[r][target_col_c] == 0 and
                          input_list[r][target_col_c1] == 0)

        if is_special_row:
            # 5. Apply Special Row Rule
            for c in range(width):
                # Check the *input* grid value for preservation logic
                if input_list[r][c] != 2:
                    output_grid[r][c] = 0
                # else: output_grid[r][c] remains its original value (which must be 2)
        else:
            # 6. Apply Normal Row Rule (only modify target columns)
            # Check output_grid value (which is currently a copy of input)
            if output_grid[r][target_col_c] != 2:
                output_grid[r][target_col_c] = 0
            if output_grid[r][target_col_c1] != 2:
                output_grid[r][target_col_c1] = 0
            # Other columns remain untouched from the initial copy

    # 7. Final Output
    return output_grid
