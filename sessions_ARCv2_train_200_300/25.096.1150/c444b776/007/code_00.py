import numpy as np
import copy

"""
Identifies horizontal and/or vertical separator lines composed entirely of the number 4.
The separator value is fixed at 4.

If a horizontal separator line is found at row index 'hr', the region of the grid above this line (rows 0 to hr-1) is considered the source pattern. This pattern is copied to the region below the separator line (rows hr+1 to end).

If a vertical separator line is found at column index 'vc', the region of the grid to the left of this line (columns 0 to vc-1) is considered the source pattern. This pattern is copied to the region to the right of the separator line (columns vc+1 to end).

If both a horizontal line (hr) and a vertical line (vc) are found, they divide the grid into four quadrants. The top-left quadrant (rows 0 to hr-1, columns 0 to vc-1) is the source pattern. This pattern is copied into the other three quadrants: top-right (rows 0 to hr-1, columns vc+1 to end), bottom-left (rows hr+1 to end, columns 0 to vc-1), and bottom-right (rows hr+1 to end, columns vc+1 to end).

The separator line(s) themselves remain unchanged in the output.
If no separator lines are found, the output grid is identical to the input grid.
When copying, if the source pattern is larger than the target region, the pattern is truncated to fit the target dimensions.
"""

def find_horizontal_separator(grid: np.ndarray, separator_value: int) -> int | None:
    """Finds the row index of the first horizontal separator line."""
    num_rows, _ = grid.shape
    for r in range(num_rows):
        # Check if all elements in the row match the separator value
        if np.all(grid[r, :] == separator_value):
            return r
    # Return None if no such row is found
    return None

def find_vertical_separator(grid: np.ndarray, separator_value: int) -> int | None:
    """Finds the column index of the first vertical separator line."""
    _, num_cols = grid.shape
    for c in range(num_cols):
         # Check if all elements in the column match the separator value
        if np.all(grid[:, c] == separator_value):
            return c
    # Return None if no such column is found
    return None

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on separator lines.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed grid.
    """
    # Convert input list of lists to a NumPy array for efficient slicing
    grid = np.array(input_grid, dtype=int)
    # Initialize output_grid as a direct copy of the input NumPy array
    output_grid = grid.copy()
    num_rows, num_cols = grid.shape
    separator_value = 4

    # Find horizontal and vertical separator lines using helper functions
    hr = find_horizontal_separator(grid, separator_value)
    vc = find_vertical_separator(grid, separator_value)

    # --- Apply transformation based on found separators ---

    # Case 1: Both horizontal and vertical separators exist
    if hr is not None and vc is not None:
        # Check if the source quadrant (top-left) actually has non-zero dimensions
        if hr > 0 and vc > 0:
            # Extract the source pattern (top-left quadrant from the original grid)
            source_pattern = grid[0:hr, 0:vc]
            source_rows, source_cols = source_pattern.shape

            # --- Replicate pattern to the other three quadrants ---

            # Target: Top-right quadrant
            tr_target_rows = hr # Height of top-right is same as top-left
            tr_target_cols = num_cols - (vc + 1) # Width is from separator+1 to end
            if tr_target_rows > 0 and tr_target_cols > 0: # Check if target exists
                # Determine the actual rows/cols to copy (minimum of source/target dims)
                copy_rows = min(source_rows, tr_target_rows)
                copy_cols = min(source_cols, tr_target_cols)
                # Perform the copy into the output grid
                output_grid[0:copy_rows, vc + 1 : vc + 1 + copy_cols] = source_pattern[0:copy_rows, 0:copy_cols]

            # Target: Bottom-left quadrant
            bl_target_rows = num_rows - (hr + 1) # Height is from separator+1 to end
            bl_target_cols = vc # Width of bottom-left is same as top-left
            if bl_target_rows > 0 and bl_target_cols > 0: # Check if target exists
                # Determine the actual rows/cols to copy
                copy_rows = min(source_rows, bl_target_rows)
                copy_cols = min(source_cols, bl_target_cols)
                # Perform the copy into the output grid
                output_grid[hr + 1 : hr + 1 + copy_rows, 0:copy_cols] = source_pattern[0:copy_rows, 0:copy_cols]

            # Target: Bottom-right quadrant
            br_target_rows = num_rows - (hr + 1) # Height is from separator+1 to end
            br_target_cols = num_cols - (vc + 1) # Width is from separator+1 to end
            if br_target_rows > 0 and br_target_cols > 0: # Check if target exists
                # Determine the actual rows/cols to copy
                copy_rows = min(source_rows, br_target_rows)
                copy_cols = min(source_cols, br_target_cols)
                # Perform the copy into the output grid
                output_grid[hr + 1 : hr + 1 + copy_rows, vc + 1 : vc + 1 + copy_cols] = source_pattern[0:copy_rows, 0:copy_cols]

    # Case 2: Only horizontal separator exists
    elif hr is not None:
        # Check if the source region (above line) actually has non-zero height
        if hr > 0:
            # Extract the source pattern (region above the horizontal line)
            source_pattern = grid[0:hr, :]
            source_rows, _ = source_pattern.shape # Only need source rows for comparison

            # Target: Region below the line
            target_rows = num_rows - (hr + 1) # Height is from separator+1 to end
            if target_rows > 0: # Check if target region exists
                # Determine the actual rows to copy (minimum of source/target height)
                copy_rows = min(source_rows, target_rows)
                # Perform the copy (all columns) into the output grid
                output_grid[hr + 1 : hr + 1 + copy_rows, :] = source_pattern[0:copy_rows, :]

    # Case 3: Only vertical separator exists
    elif vc is not None:
         # Check if the source region (left of line) actually has non-zero width
        if vc > 0:
            # Extract the source pattern (region left of the vertical line)
            source_pattern = grid[:, 0:vc]
            _, source_cols = source_pattern.shape # Only need source cols for comparison

            # Target: Region right of the line
            target_cols = num_cols - (vc + 1) # Width is from separator+1 to end
            if target_cols > 0: # Check if target region exists
                # Determine the actual columns to copy (minimum of source/target width)
                copy_cols = min(source_cols, target_cols)
                # Perform the copy (all rows) into the output grid
                output_grid[:, vc + 1 : vc + 1 + copy_cols] = source_pattern[:, 0:copy_cols]

    # Case 4: No separators found
    # No action needed, output_grid remains the initial copy of the input grid

    # Convert the final NumPy array back to a standard list of lists before returning
    return output_grid.tolist()