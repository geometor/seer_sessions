import numpy as np

def _find_nearest_5_left(grid_row, c):
    """Find the column index of the nearest 5 to the left in a row."""
    for c_left in range(c - 1, -1, -1):
        if grid_row[c_left] == 5:
            return c_left
    return None

def _find_nearest_5_right(grid_row, c, cols):
    """Find the column index of the nearest 5 to the right in a row."""
    for c_right in range(c + 1, cols):
        if grid_row[c_right] == 5:
            return c_right
    return None

def _find_nearest_5_up(grid_col, r):
    """Find the row index of the nearest 5 above in a column."""
    for r_up in range(r - 1, -1, -1):
        if grid_col[r_up] == 5:
            return r_up
    return None

def _find_nearest_5_down(grid_col, r, rows):
    """Find the row index of the nearest 5 below in a column."""
    for r_down in range(r + 1, rows):
        if grid_col[r_down] == 5:
            return r_down
    return None

def _is_path_clear_horizontal(grid_row, c_left, c_right):
    """Check if the horizontal path between c_left and c_right contains only 0s."""
    return np.all(grid_row[c_left + 1 : c_right] == 0)

def _is_path_clear_vertical(grid_col, r_up, r_down):
    """Check if the vertical path between r_up and r_down contains only 0s."""
    return np.all(grid_col[r_up + 1 : r_down] == 0)

def transform(input_grid):
    """
    Transforms the input grid. A cell with value 0 is changed to 1 if it lies on
    a straight horizontal or vertical line segment between two cells with value 5,
    and all cells on that segment (excluding the endpoints) are 0s in the input.
    Cells with value 5 remain unchanged. Cells with value 0 not meeting the
    path criteria remain 0.
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
            # Only consider cells that are 0 in the input
            if input_arr[r, c] == 0:
                
                # --- Check Horizontally ---
                c_left = _find_nearest_5_left(input_arr[r, :], c)
                c_right = _find_nearest_5_right(input_arr[r, :], c, cols)

                # Check if 5s were found on both sides and the path between them is clear
                if c_left is not None and c_right is not None:
                    if _is_path_clear_horizontal(input_arr[r, :], c_left, c_right):
                        output_arr[r, c] = 1
                        continue # Cell changed, move to the next cell

                # --- Check Vertically (only if horizontal check didn't change the cell) ---
                r_up = _find_nearest_5_up(input_arr[:, c], r)
                r_down = _find_nearest_5_down(input_arr[:, c], r, rows)

                # Check if 5s were found above and below and the path between them is clear
                if r_up is not None and r_down is not None:
                     if _is_path_clear_vertical(input_arr[:, c], r_up, r_down):
                        output_arr[r, c] = 1
                        # No need for continue here as it's the last check for this cell

    # Return the modified grid, converted back to list of lists
    return output_arr.tolist()