import numpy as np

# Helper functions for finding nearest 5s and checking path clarity

def _find_nearest_5_left(grid_row, c):
    """Find the column index of the nearest 5 to the left in a row."""
    for c_left in range(c - 1, -1, -1):
        if grid_row[c_left] == 5:
            return c_left
    return None # Return None if no 5 is found to the left

def _find_nearest_5_right(grid_row, c, cols):
    """Find the column index of the nearest 5 to the right in a row."""
    for c_right in range(c + 1, cols):
        if grid_row[c_right] == 5:
            return c_right
    return None # Return None if no 5 is found to the right

def _find_nearest_5_up(grid_col, r):
    """Find the row index of the nearest 5 above in a column."""
    for r_up in range(r - 1, -1, -1):
        if grid_col[r_up] == 5:
            return r_up
    return None # Return None if no 5 is found above

def _find_nearest_5_down(grid_col, r, rows):
    """Find the row index of the nearest 5 below in a column."""
    for r_down in range(r + 1, rows):
        if grid_col[r_down] == 5:
            return r_down
    return None # Return None if no 5 is found below

def _is_path_clear_horizontal(grid_row, c_left, c_right):
    """Check if the horizontal path between c_left and c_right (exclusive) contains only 0s."""
    # If indices are adjacent or the same, path is clear (no cells between)
    if c_right <= c_left + 1:
        return True
    # Check if all cells strictly between c_left and c_right are 0
    return np.all(grid_row[c_left + 1 : c_right] == 0)

def _is_path_clear_vertical(grid_col, r_up, r_down):
    """Check if the vertical path between r_up and r_down (exclusive) contains only 0s."""
    # If indices are adjacent or the same, path is clear (no cells between)
    if r_down <= r_up + 1:
        return True
    # Check if all cells strictly between r_up and r_down are 0
    return np.all(grid_col[r_up + 1 : r_down] == 0)

def transform(input_grid):
    """
    Transforms the input grid based on the "clear path" rule.
    A cell with value 0 is changed to 1 if it lies on a straight horizontal or
    vertical line segment between two cells with value 5 in the input grid,
    and all cells strictly between those two 5s along that segment are 0s in the input grid.
    Cells with value 5 remain unchanged. Cells with value 0 that do not meet
    the path criteria remain 0.
    Note: This implementation reflects the rule derived from examples 1-3, which
    differs from the expected output of example 4 at one specific cell.
    """
    # Convert input to numpy array for efficient operations
    input_arr = np.array(input_grid, dtype=int)
    rows, cols = input_arr.shape

    # Initialize output_grid as a copy of the input grid
    # We will modify this grid based on the rules
    output_arr = np.copy(input_arr)

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Only consider cells that are 0 in the input grid
            if input_arr[r, c] == 0:

                # --- Check Horizontally ---
                # Find nearest 5s to the left and right in the current row
                c_left = _find_nearest_5_left(input_arr[r, :], c)
                c_right = _find_nearest_5_right(input_arr[r, :], c, cols)

                # Check if 5s were found on both sides
                if c_left is not None and c_right is not None:
                    # Check if the current cell (r, c) is actually between the found 5s
                    # and if the path between the 5s (exclusive endpoints) is clear (only 0s)
                    if c_left < c < c_right and _is_path_clear_horizontal(input_arr[r, :], c_left, c_right):
                        # If conditions met, change the cell to 1 in the output grid
                        output_arr[r, c] = 1
                        # Move to the next cell as the condition is met horizontally
                        continue

                # --- Check Vertically (only if horizontal check didn't change the cell to 1) ---
                # Find nearest 5s above and below in the current column
                r_up = _find_nearest_5_up(input_arr[:, c], r)
                r_down = _find_nearest_5_down(input_arr[:, c], r, rows)

                # Check if 5s were found above and below
                if r_up is not None and r_down is not None:
                    # Check if the current cell (r, c) is actually between the found 5s
                    # and if the path between the 5s (exclusive endpoints) is clear (only 0s)
                    if r_up < r < r_down and _is_path_clear_vertical(input_arr[:, c], r_up, r_down):
                        # If conditions met, change the cell to 1 in the output grid
                        output_arr[r, c] = 1
                        # No continue needed here as it's the last check for this cell

            # Cells that started as 5 remain 5 (due to initial copy)
            # Cells that started as 0 and didn't meet path conditions remain 0 (due to initial copy)

    # Return the modified grid, converted back to list of lists format
    return output_arr.tolist()