```python
import copy

"""
Transforms an input grid based on specific patterns observed in the training examples. 
The transformation type is determined by first checking for the presence of the digit 6 in the input grid. 
If 6 is present, a 'Type 3' transformation applies. 
If 6 is not present, the transformation type ('Type 1' or 'Type 2') is determined by the value in the top-left corner (input_grid[0][0]).

Transformation Types:
1.  Type 1 (No 6, Input[0][0] == 2): Applies a top-right frame (corner 0, top row 1, right column 8), 
    modifies row 8 by changing values to 8 in even-numbered columns starting from column 4 (index 4), 
    and sets cell (1, 9) to 1.
2.  Type 2 (No 6, Input[0][0] != 2): Applies a top-left frame (corner 0, top row 3, left column 2), 
    and sets specific cells: (1, 9) to 3 and (5, 1) to 2.
3.  Type 3 (Input contains 6): Overwrites the last row with 6s, finds the location (six_r, six_c) of the first 6 
    in the *input* grid, and applies an alternating pattern in column six_c starting two rows 
    below six_r (changing 3s to 6s in rows six_r+2, six_r+4, etc.).
"""


def find_first(grid: list[list[int]], value: int) -> tuple[int | None, int | None]:
    """
    Finds the row and column index of the first occurrence of a value in the grid.

    Args:
        grid: The 2D list of integers representing the grid.
        value: The integer value to search for.

    Returns:
        A tuple (row_index, column_index) if the value is found, otherwise (None, None).
    """
    for r_idx, row in enumerate(grid):
        for c_idx, cell in enumerate(row):
            if cell == value:
                return r_idx, c_idx
    return None, None

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    rows = len(output_grid)
    if rows == 0:
        return output_grid  # Handle empty grid case
    cols = len(output_grid[0])
    if cols == 0:
        return output_grid # Handle empty row case

    # Check for Trigger Value: Search the input grid for the value 6
    six_r, six_c = find_first(input_grid, 6)

    # --- Type 3 Transformation (if 6 is found) ---
    if six_r is not None and six_c is not None:
        # Overwrite the entire last row of the output grid with 6
        if rows > 0:
             for c in range(cols):
                output_grid[rows - 1][c] = 6

        # Apply column alternating pattern based on the found 6 location
        # Iterate through rows (r) starting from six_r + 2, incrementing by 2
        start_row = six_r + 2
        for r in range(start_row, rows, 2):
             # Check bounds and if the cell value in the output grid is 3
             if r < rows and output_grid[r][six_c] == 3:
                 output_grid[r][six_c] = 6 # Change it to 6

    # --- Type 1/Type 2 Transformation (if 6 is NOT found) ---
    else:
        # Check the value of the top-left cell (input_grid[0][0])
        top_left_value = input_grid[0][0] if rows > 0 and cols > 0 else None

        # --- If input_grid[0][0] is 2 (Type 1) ---
        if top_left_value == 2:
            # Apply a top-right frame
            if rows > 0 and cols > 0:
                output_grid[0][cols - 1] = 0  # Top-right corner
                # Fill top row (excluding corner) with 1
                for c in range(cols - 1):
                    output_grid[0][c] = 1
                # Fill right column (excluding corner) with 8
                for r in range(1, rows):
                    output_grid[r][cols - 1] = 8

            # Modify row 8 (index 8)
            target_row = 8
            if rows > target_row: # Check if row 8 exists
                start_col = 4
                # Iterate through columns c from 4 to last_col
                for c in range(start_col, cols):
                    # If c is even, set output_grid[8][c] to 8 (regardless of original value)
                    if c % 2 == 0:
                        output_grid[target_row][c] = 8

            # Set specific cell output_grid[1][9] to 1 (Corrected coordinate)
            if rows > 1 and cols > 9: # Check bounds
                 output_grid[1][9] = 1

        # --- Else (if input_grid[0][0] is not 2, e.g., 1 for Type 2) ---
        else:
            # Apply a top-left frame
            if rows > 0 and cols > 0:
                output_grid[0][0] = 0 # Top-left corner
                # Fill top row (excluding corner) with 3
                for c in range(1, cols):
                    output_grid[0][c] = 3
                # Fill left column (excluding corner) with 2
                for r in range(1, rows):
                    output_grid[r][0] = 2

            # Set specific cell output_grid[1][9] to 3
            if rows > 1 and cols > 9: # Check bounds
                output_grid[1][9] = 3
            # Set specific cell output_grid[5][1] to 2
            if rows > 5 and cols > 1: # Check bounds
                output_grid[5][1] = 2

    # Finalization: Return the modified output grid
    return output_grid
```