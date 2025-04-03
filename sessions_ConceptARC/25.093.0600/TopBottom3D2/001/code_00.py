import copy

"""
Modifies an input grid by identifying a specific column and zeroing out one of its digits.
The target column is the unique column containing exactly two distinct non-zero digits. 
One of these digits must be a digit that appears as the sole non-zero digit in at least one row (a 'uniform row digit'). 
The other digit in the target column (the one not found in uniform rows) is the digit to be zeroed out within that column.
"""

def _get_distinct_non_zero(values):
  """Finds the set of distinct non-zero values in a list."""
  return set(v for v in values if v != 0)

def _find_uniform_row_digits(grid):
  """Identifies the set of non-zero digits that characterize 'uniform rows'.
  A uniform row contains exactly one distinct non-zero digit.
  """
  uniform_digits = set()
  for row in grid:
    distinct_digits = _get_distinct_non_zero(row)
    if len(distinct_digits) == 1:
      uniform_digits.add(list(distinct_digits)[0])
  return uniform_digits

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Create a deep copy of the input grid to modify
    output_grid = copy.deepcopy(input_grid)
    if not input_grid:
        return output_grid # Handle empty grid case

    num_rows = len(input_grid)
    if num_rows == 0:
        return output_grid
    num_cols = len(input_grid[0])
    if num_cols == 0:
         return output_grid # Handle empty row case


    # 1. Find the set of digits that define 'uniform rows'
    uniform_digits = _find_uniform_row_digits(input_grid)

    # 2. Iterate through columns to find the target column and the digit to remove
    target_col_index = -1
    digit_to_remove = -1

    for c in range(num_cols):
        # Extract the current column
        column_values = [input_grid[r][c] for r in range(num_rows)]
        # Find distinct non-zero digits in this column
        distinct_col_digits = _get_distinct_non_zero(column_values)

        # Check if the column meets the criteria (exactly 2 distinct non-zero digits)
        if len(distinct_col_digits) == 2:
            d1, d2 = list(distinct_col_digits)
            # Check if one digit is uniform and the other is not
            if (d1 in uniform_digits and d2 not in uniform_digits):
                target_col_index = c
                digit_to_remove = d2
                break # Found the target column
            elif (d2 in uniform_digits and d1 not in uniform_digits):
                target_col_index = c
                digit_to_remove = d1
                break # Found the target column

    # 3. Modify the output grid if a target column and digit were found
    if target_col_index != -1 and digit_to_remove != -1:
        for r in range(num_rows):
            if output_grid[r][target_col_index] == digit_to_remove:
                output_grid[r][target_col_index] = 0

    # Return the modified grid
    return output_grid