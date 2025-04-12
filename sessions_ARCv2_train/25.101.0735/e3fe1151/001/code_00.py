"""
Transforms a 5x5 grid of integers based on the following rules:
1. Initialize the output grid as a copy of the input grid.
2. Iterate through each cell (r, c) of the input grid.
3. Identify 'target' cells: cells containing the digit '7' that are outside the central cross (i.e., r != 2 and c != 2).
4. For each target cell:
    a. Find the symmetrically opposite cell coordinates (sr = 4 - r, sc = 4 - c).
    b. Get the value of the symmetrical cell from the *input* grid (sym_val = input[sr][sc]).
    c. If sym_val is NOT 7, update the output grid at (r, c) with sym_val.
    d. If sym_val IS 7 (fallback rule):
        i. If the target cell's row r is less than 2 (top half), update the output grid at (r, c) with the value from the input grid's bottom-left corner (input[4][0]).
        ii. If the target cell's row r is greater than 2 (bottom half), update the output grid at (r, c) with the value from the input grid's top-right corner (input[0][4]).
5. Cells that are not target cells (i.e., not '7' or are on the central cross) remain unchanged.
6. Return the final output grid.
"""

import copy # Used for deep copying the grid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a transformation rule to a 5x5 grid based on symmetrical cell values
    and corner values for specific '7' cells outside the central cross.
    """
    # Ensure the grid is 5x5, although the logic assumes this implicitly
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if rows != 5 or cols != 5:
        # Or raise an error, depending on desired behavior for invalid input size
        print("Warning: Input grid is not 5x5. Logic may not apply correctly.")
        # Attempt to proceed anyway, might fail if indices go out of bounds

    # Initialize output_grid as a deep copy of input_grid to avoid modifying the input
    # during symmetrical lookups.
    output_grid = copy.deepcopy(input_grid)

    # Define the marker digit and grid dimensions (0-indexed max)
    marker_digit = 7
    max_idx = 4 # for 5x5 grid

    # Retrieve corner values needed for the fallback rule
    bottom_left_corner_val = input_grid[max_idx][0]
    top_right_corner_val = input_grid[0][max_idx]

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the cell is a 'target' cell:
            # - Contains the marker digit (7)
            # - Is outside the central cross (row 2 and column 2)
            if input_grid[r][c] == marker_digit and r != 2 and c != 2:
                # Find the coordinates of the symmetrically opposite cell
                sr = max_idx - r
                sc = max_idx - c

                # Get the value of the symmetrical cell from the *input* grid
                sym_val = input_grid[sr][sc]

                # Apply the main transformation rule
                if sym_val != marker_digit:
                    output_grid[r][c] = sym_val
                # Apply the fallback rule if the symmetrical cell is also a marker digit
                else:
                    # Check if the target cell is in the top half (rows 0, 1)
                    if r < 2:
                        output_grid[r][c] = bottom_left_corner_val
                    # Check if the target cell is in the bottom half (rows 3, 4)
                    elif r > 2:
                         output_grid[r][c] = top_right_corner_val
                    # Note: The middle row (r=2) is excluded by the initial 'target cell' check,
                    # so we don't need an explicit condition for it here.

            # If the cell is not a target cell, its value remains unchanged
            # (already handled by the initial deep copy).

    return output_grid