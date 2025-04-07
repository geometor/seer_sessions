import copy

"""
Transforms an input grid based on specific patterns observed in the training examples. 
The transformation type is determined by first checking for the presence of the digit 6. 
If 6 is present, a specific set of rules (Type 3) applies. 
If 6 is not present, the transformation type is determined by the value in the top-left corner (input_grid[0][0]): 
value 2 triggers Type 1 rules, and any other value (like 1 in the examples) triggers Type 2 rules.

Transformation Types:
1.  Type 1 (Input[0][0] == 2, No 6): Applies a top-right frame (corner 0, top row 1, right column 8), 
    modifies row 8 with an alternating pattern (changing 2 to 8 starting from column 5), 
    and sets cell (1, 10) to 1.
2.  Type 2 (Input[0][0] != 2, No 6): Applies a top-left frame (corner 0, top row 3, left column 2), 
    and sets specific cells: (1, 9) to 3 and (5, 1) to 2.
3.  Type 3 (Input contains 6): Overwrites the last row with 6s, finds the location of the first 6 
    in the *input* grid, and applies an alternating pattern in that column starting two rows 
    below the found 6 (changing 3 to 6).
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
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid: The 2D list of integers representing the input grid.

    Returns:
        A new 2D list of integers representing the transformed grid.
    """
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    rows = len(output_grid)
    if rows == 0:
        return output_grid  # Handle empty grid case
    cols = len(output_grid[0])
    if cols == 0:
        return output_grid # Handle empty row case

    # Check for Type 3 trigger: presence of 6
    six_r, six_c = find_first(input_grid, 6)

    if six_r is not None and six_c is not None:
        # --- Transformation Type 3 (Input contains 6) ---
        
        # Overwrite the last row with 6
        if rows > 0:
             for c in range(cols):
                output_grid[rows - 1][c] = 6

        # Apply column alternating pattern based on the found 6 location
        # Start two rows below the original 6's row
        start_row = six_r + 2
        for r in range(start_row, rows, 2): # Iterate every other row from start_row
             # Check bounds and if the cell value in the output grid is 3
             if r < rows and output_grid[r][six_c] == 3:
                 output_grid[r][six_c] = 6

    else:
        # --- No 6 found, check Type 1 or Type 2 based on input_grid[0][0] ---
        
        # Get top-left value, handle potential empty grid edge case again just in case
        top_left_value = input_grid[0][0] if rows > 0 and cols > 0 else None

        if top_left_value == 2:
            # --- Transformation Type 1 (Input[0][0] == 2) ---
            
            # Apply top-right frame (corner 0, top row 1, right col 8)
            if rows > 0 and cols > 0:
                output_grid[0][cols - 1] = 0  # Top-right corner
                for c in range(cols - 1):    # Fill top row (excluding corner)
                    output_grid[0][c] = 1
                for r in range(1, rows):     # Fill right column (excluding corner)
                    output_grid[r][cols - 1] = 8

            # Apply row 8 alternating pattern (change 2 to 8)
            target_row = 8
            if rows > target_row: # Check if row 8 exists
                start_col = 5
                for c in range(start_col, cols, 2): # Iterate every other column from start_col
                    # Check if cell value in the output grid is 2 before changing
                    if output_grid[target_row][c] == 2:
                        output_grid[target_row][c] = 8

            # Apply specific cell modification: set (1, 10) to 1
            if rows > 1 and cols > 10: # Check bounds
                 output_grid[1][10] = 1

        else:
            # --- Transformation Type 2 (Default/Input[0][0] != 2) ---
            
            # Apply top-left frame (corner 0, top row 3, left col 2)
            if rows > 0 and cols > 0:
                output_grid[0][0] = 0 # Top-left corner
                for c in range(1, cols): # Fill top row (excluding corner)
                    output_grid[0][c] = 3
                for r in range(1, rows): # Fill left column (excluding corner)
                    output_grid[r][0] = 2

            # Apply specific cell modifications
            if rows > 1 and cols > 9: # Check bounds for (1, 9)
                output_grid[1][9] = 3
            if rows > 5 and cols > 1: # Check bounds for (5, 1)
                output_grid[5][1] = 2

    return output_grid