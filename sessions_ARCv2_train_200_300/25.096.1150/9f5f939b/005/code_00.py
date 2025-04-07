import copy

"""
Transforms a 2D grid by replacing specific '8' values with '4'.
An '8' at position (r, c) is changed to a '4' if and only if all the following conditions are met:
1. The horizontal sequence of 7 cells starting at column c-3 in row r matches [1, 1, 8, 8, 8, 1, 1].
2. The cell directly above it, at (r-1, c), is also an '8'.
3. Another matching pattern [1, 1, 8, 8, 8, 1, 1] does *not* start 5 columns after the first pattern's start, i.e., at column (c-3) + 5 = c+2 in the same row r.
"""

def _check_pattern(grid_row, start_col, pattern):
    """Checks if the pattern exists at the specified location in the row."""
    pattern_len = len(pattern)
    num_cols = len(grid_row)
    # Check if the pattern fits within the row boundaries from start_col
    if start_col < 0 or start_col + pattern_len > num_cols:
        return False
    # Check if the slice matches the pattern
    return grid_row[start_col : start_col + pattern_len] == pattern

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the 2D input grid.

    Returns:
        A list of lists representing the transformed 2D output grid.
    """
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)

    # Get grid dimensions
    num_rows = len(input_grid)
    if num_rows < 2:  # Need at least 2 rows to check the cell above
        return output_grid
    num_cols = len(input_grid[0])
    if num_cols == 0:
        return output_grid # Handle empty row case

    # Define the specific horizontal pattern and its properties
    pattern = [1, 1, 8, 8, 8, 1, 1]
    pattern_len = len(pattern)
    # Define the index within the pattern corresponding to the '8' that might change
    # This is index 3 (0-based) within the pattern.
    target_index_in_pattern = 3
    # Define the offset for the suppression check pattern start
    suppression_offset = 5

    # If the grid columns are fewer than the pattern length, no transformation is possible
    if num_cols < pattern_len:
        return output_grid

    # Iterate through each row, starting from the second row (index 1)
    for r in range(1, num_rows):
        # Iterate through possible *target* column indices 'c' for the central '8'
        # The pattern starts at c - target_index_in_pattern
        # The loop needs to ensure the full pattern fits:
        # Start index: c - target_index_in_pattern >= 0  => c >= target_index_in_pattern
        # End index: (c - target_index_in_pattern) + pattern_len <= num_cols
        #            c + pattern_len - target_index_in_pattern <= num_cols
        #            c <= num_cols - pattern_len + target_index_in_pattern
        min_c = target_index_in_pattern
        max_c = num_cols - pattern_len + target_index_in_pattern

        for c in range(min_c, max_c + 1):
            # Calculate the starting column index for the primary pattern check
            pattern_start_col = c - target_index_in_pattern

            # Condition 1: Check if the primary pattern matches
            pattern_found = _check_pattern(input_grid[r], pattern_start_col, pattern)

            if pattern_found:
                # Condition 2: Check if the cell above the target '8' is also '8'
                # The target '8' is at index 'c'
                cell_above_is_8 = (input_grid[r-1][c] == 8)

                if cell_above_is_8:
                    # Condition 3: Check for the suppressing pattern
                    suppression_pattern_start_col = pattern_start_col + suppression_offset
                    suppression_found = _check_pattern(input_grid[r], suppression_pattern_start_col, pattern)

                    # If the suppressing pattern is NOT found, then apply the change
                    if not suppression_found:
                        output_grid[r][c] = 4 # Change the target '8' to '4'

    # Return the modified grid
    return output_grid