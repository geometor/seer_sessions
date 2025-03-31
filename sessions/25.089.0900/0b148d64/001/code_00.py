import numpy as np

"""
Extract the lower pattern from an input grid, where patterns are separated by horizontal white space.

1.  Scan the input grid row by row from top to bottom.
2.  Identify the first contiguous block of one or more rows where all pixels are white (0). Record the row index of the *last* row in this separator block.
3.  Consider only the rows *below* this separator block.
4.  Find the minimum row index (`row_start`) and maximum row index (`row_end`) of rows in this lower section that contain at least one non-white pixel.
5.  Within the rows from `row_start` to `row_end` (inclusive), find the minimum column index (`col_start`) and maximum column index (`col_end`) that contain a non-white pixel.
6.  Extract the subgrid from the input grid starting at `row_start`, ending at `row_end`, starting at `col_start`, and ending at `col_end`. This extracted subgrid is the output.
"""

def find_separator_end_row(grid_np):
    """Finds the index of the last row of the first horizontal block of all-white rows."""
    in_separator = False
    separator_end_row = -1
    num_rows = grid_np.shape[0]

    for r in range(num_rows):
        is_all_white = np.all(grid_np[r, :] == 0)
        if is_all_white:
            if not in_separator:
                in_separator = True # Start of a potential separator block
            separator_end_row = r # Update the end row as long as we see white rows
        elif in_separator:
            # We found a non-white row *after* being in a separator block
            return separator_end_row # The previous row was the end
        # else: not in separator and not all white, continue scanning

    # If the grid ends with a separator block
    if in_separator:
        return separator_end_row

    # Should not happen based on task description, but return -1 if no separator found
    return -1 

def find_bounding_box(grid_np):
    """Finds the bounding box (min_row, max_row, min_col, max_col) of non-white pixels."""
    non_white_coords = np.argwhere(grid_np != 0)
    if non_white_coords.size == 0:
        return None # No non-white pixels
    min_row = np.min(non_white_coords[:, 0])
    max_row = np.max(non_white_coords[:, 0])
    min_col = np.min(non_white_coords[:, 1])
    max_col = np.max(non_white_coords[:, 1])
    return min_row, max_row, min_col, max_col


def transform(input_grid):
    """
    Extracts the lower pattern from an input grid separated by white space.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    num_rows, num_cols = grid_np.shape

    # 1 & 2. Find the end row of the separator block
    separator_end = find_separator_end_row(grid_np)

    # Handle case where no separator is found (though unlikely per examples)
    if separator_end == -1 or separator_end == num_rows - 1:
        # No separator or separator is at the very bottom, meaning no lower pattern
        # Or maybe the lower pattern starts immediately after? Let's assume no lower pattern.
        # Returning an empty grid might be appropriate, or perhaps the original grid
        # if the rules were different. Based on examples, a separator exists.
        # If the separator is the last row, there's nothing below it.
        return [] 

    # 3. Define the region below the separator
    lower_region_start_row = separator_end + 1
    lower_region_np = grid_np[lower_region_start_row:, :]

    # Check if the lower region is empty
    if lower_region_np.shape[0] == 0:
         return [] # No rows below separator

    # 4 & 5. Find the bounding box of non-white pixels *within the lower region*
    bounding_box = find_bounding_box(lower_region_np)

    # Handle case where the lower region is all white
    if bounding_box is None:
        return [] # No pattern found below separator

    min_r_local, max_r_local, min_c, max_c = bounding_box

    # 6. Extract the subgrid defined by the bounding box from the lower region
    # Note: The row indices from find_bounding_box are relative to lower_region_np
    output_grid_np = lower_region_np[min_r_local : max_r_local + 1, min_c : max_c + 1]

    # Convert back to list of lists
    output_grid = output_grid_np.tolist()

    return output_grid