import copy

"""
Transforms an input grid of digits based on the presence and location of '8's and '2's.

The rules are applied hierarchically:

1.  Initialize the output grid as an identical copy of the input grid.
2.  Scan the input grid to find all locations of the digit '8' and the digit '2'. Determine if '8' (`has_8`) and '2' (`has_2`) are present.
3.  If `has_8` is true:
    a.  Find the maximum column index (`C_max8`) where an '8' appears.
    b.  Find the minimum row index (`R_first_any8`) containing any '8'.
    c.  Find the minimum row index (`R_first_max8`) containing an '8' specifically in column `C_max8`.
    d.  If `R_first_any8` is equal to `R_first_max8`:
        i.  If `has_2` is also true:
            1. Find the maximum row index (`R_last2`) containing a '2'.
            2. Find the column index (`C_last2`) of the first '2' encountered (minimum column index) in row `R_last2`.
            3. Calculate the target column `C_target = C_last2 + 2`.
            4. If the cell `(R_last2, C_target)` is within the grid boundaries, change its value to '5' in the output grid.
        ii. If `has_2` is false:
            1. Calculate the target column `C_target = C_max8 + 2`.
            2. Set the starting row index `R_start = 1`.
            3. Iterate through rows `R` from `R_start` to the last row index. If the cell `(R, C_target)` is within grid boundaries, change its value to '5' in the output grid.
    e.  If `R_first_any8` is NOT equal to `R_first_max8`:
        i.  Calculate the target column `C_target = C_max8 + 2`.
        ii. Calculate the starting row index `R_start = max(0, R_first_max8 - 1)`.
        iii. Iterate through rows `R` from `R_start` to the last row index. If the cell `(R, C_target)` is within grid boundaries, change its value to '5' in the output grid.
4.  If `has_8` is false, but `has_2` is true:
    a.  Find the maximum row index (`R_last2`) containing a '2'.
    b.  Find the column index (`C_last2`) of the first '2' encountered (minimum column index) in row `R_last2`.
    c.  Calculate the target column `C_target = C_last2 + 2`.
    d.  If the cell `(R_last2, C_target)` is within the grid boundaries, change its value to '5' in the output grid.
5.  If neither '8' nor '2' is present: The output grid remains unchanged.
6.  Return the final output grid.
"""

def _find_digit_locations(grid: list[list[int]], digit: int) -> list[tuple[int, int]]:
    """Finds all (row, col) coordinates of a given digit in the grid."""
    locations = []
    for r, row in enumerate(grid):
        for c, cell_value in enumerate(row):
            if cell_value == digit:
                locations.append((r, c))
    return locations

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid.
    """
    # Handle empty or invalid input
    if not input_grid or not input_grid[0]:
        return copy.deepcopy(input_grid) # Return copy of empty/invalid input

    num_rows = len(input_grid)
    num_cols = len(input_grid[0])
    
    # Initialize output_grid as a deep copy
    output_grid = copy.deepcopy(input_grid)

    # Find locations of '8' and '2'
    locations_8 = _find_digit_locations(input_grid, 8)
    locations_2 = _find_digit_locations(input_grid, 2)
    has_8 = bool(locations_8)
    has_2 = bool(locations_2)

    # Rule 1: '8' is present
    if has_8:
        # Calculate C_max8: maximum column index of any '8'
        C_max8 = -1
        for r, c in locations_8:
            if c > C_max8:
                C_max8 = c
        
        # Calculate R_first_any8: minimum row index of any '8'
        R_first_any8 = num_rows # Initialize higher than possible index
        for r, c in locations_8:
            if r < R_first_any8:
                R_first_any8 = r
        
        # Calculate R_first_max8: minimum row index of '8' in column C_max8
        R_first_max8 = num_rows # Initialize higher than possible index
        for r, c in locations_8:
            if c == C_max8 and r < R_first_max8:
                R_first_max8 = r
        
        # Check if C_max8 and R_first_max8 were actually found (should be true if has_8)
        if C_max8 == -1 or R_first_max8 == num_rows:
            # This case should ideally not happen if has_8 is true, but handle defensively
            return output_grid

        # Rule 1.d: R_first_any8 == R_first_max8
        if R_first_any8 == R_first_max8:
            # Rule 1.d.i: '2' is also present
            if has_2:
                # Find R_last2: maximum row index of any '2'
                R_last2 = -1
                for r, c in locations_2:
                    if r > R_last2:
                        R_last2 = r
                
                # Find C_last2: minimum column index of '2' in row R_last2
                C_last2 = num_cols # Initialize higher than possible index
                found_c_last2 = False
                if R_last2 != -1:
                    for r, c in locations_2:
                        if r == R_last2 and c < C_last2:
                            C_last2 = c
                            found_c_last2 = True
                
                # If R_last2 and C_last2 are valid
                if R_last2 != -1 and found_c_last2:
                    # Calculate C_target based on '2'
                    C_target = C_last2 + 2
                    # Modify the single cell if C_target is within bounds
                    if 0 <= R_last2 < num_rows and 0 <= C_target < num_cols:
                        output_grid[R_last2][C_target] = 5
            # Rule 1.d.ii: '2' is NOT present
            else:
                # Calculate C_target based on '8'
                C_target = C_max8 + 2
                # Check if C_target is within grid bounds
                if C_target < num_cols:
                    # Set start row
                    R_start = 1 
                    # Modify column C_target from R_start downwards
                    for r in range(R_start, num_rows):
                         # Check row bounds just in case, though range handles upper bound
                         if 0 <= r < num_rows: # Ensure row is valid
                            output_grid[r][C_target] = 5

        # Rule 1.e: R_first_any8 != R_first_max8
        else:
            # Calculate C_target based on '8'
            C_target = C_max8 + 2
            # Check if C_target is within grid bounds
            if C_target < num_cols:
                # Calculate start row
                R_start = max(0, R_first_max8 - 1) 
                # Modify column C_target from R_start downwards
                for r in range(R_start, num_rows):
                    # Check row bounds just in case
                    if 0 <= r < num_rows: # Ensure row is valid
                        output_grid[r][C_target] = 5

    # Rule 4: '8' is NOT present, but '2' IS present
    elif has_2:
        # Find R_last2: maximum row index of any '2'
        R_last2 = -1
        for r, c in locations_2:
            if r > R_last2:
                R_last2 = r
        
        # Find C_last2: minimum column index of '2' in row R_last2 
        C_last2 = num_cols # Initialize higher than possible index
        found_c_last2 = False
        if R_last2 != -1:
            for r, c in locations_2:
                if r == R_last2 and c < C_last2:
                    C_last2 = c
                    found_c_last2 = True
        
        # Proceed if both R_last2 and C_last2 were found
        if R_last2 != -1 and found_c_last2:
            # Calculate C_target from '2'
            C_target = C_last2 + 2
            
            # Modify the single cell if C_target is within bounds
            if 0 <= R_last2 < num_rows and 0 <= C_target < num_cols:
                output_grid[R_last2][C_target] = 5

    # Rule 5: Neither '8' nor '2' is present - No changes needed

    return output_grid