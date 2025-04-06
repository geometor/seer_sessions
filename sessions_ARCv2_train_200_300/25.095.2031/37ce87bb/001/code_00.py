"""
Transforms an input grid of digits based on the presence and location of '8's and '2's.

1.  Initialize the output grid as a copy of the input grid.
2.  Check if the digit '8' exists in the input grid.
3.  If '8' is present:
    a.  Find the maximum column index (C_max8) where an '8' appears.
    b.  Calculate the target column (C_target = C_max8 + 2).
    c.  Find the minimum row index (R_first_any8) containing any '8'.
    d.  Find the minimum row index (R_first_max8) containing an '8' specifically in column C_max8.
    e.  Determine the starting row (R_start):
        i.  If R_first_any8 equals R_first_max8, R_start = 1.
        ii. Otherwise, R_start = R_first_max8 - 1.
    f.  Modify the output grid: For each row R from R_start down to the last row, change the digit at column C_target to '5', if the target cell is within grid bounds.
4.  If '8' is NOT present:
    a.  Check if the digit '2' exists in the input grid.
    b.  If '2' is present:
        i.  Find the maximum row index (R_last2) where a '2' appears.
        ii. Find the column index (C_2) of the '2' in row R_last2 (assuming one '2' per row or taking the first).
        iii. Calculate the target column (C_target = C_2 + 2).
        iv. Modify the output grid: Change the digit at (R_last2, C_target) to '5', if the target cell is within grid bounds.
5.  If neither '8' nor '2' is present, the output grid remains unchanged.
6.  Return the modified output grid.
"""

import copy

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
    # initialize output_grid as a deep copy
    output_grid = copy.deepcopy(input_grid)
    if not input_grid:
        return output_grid
        
    num_rows = len(input_grid)
    if num_rows == 0:
        return output_grid
    num_cols = len(input_grid[0])
    if num_cols == 0:
        return output_grid

    # Find locations of '8'
    locations_8 = _find_digit_locations(input_grid, 8)

    # perform transformations based on '8' or '2'
    if locations_8:
        # Case 1: '8' is present
        
        # Find C_max8: maximum column index of any '8'
        C_max8 = -1
        for r, c in locations_8:
            if c > C_max8:
                C_max8 = c
        
        # Calculate C_target
        C_target = C_max8 + 2

        # Check if C_target is within grid bounds
        if C_target < num_cols:
            # Find R_first_any8: minimum row index of any '8'
            R_first_any8 = num_rows 
            for r, c in locations_8:
                if r < R_first_any8:
                    R_first_any8 = r
            
            # Find R_first_max8: minimum row index of '8' in column C_max8
            R_first_max8 = num_rows
            for r, c in locations_8:
                if c == C_max8 and r < R_first_max8:
                    R_first_max8 = r

            # Determine R_start
            R_start = 0 # Default value, should be updated
            if R_first_any8 == R_first_max8:
                R_start = 1
            else:
                R_start = R_first_max8 - 1 # Ensure this doesn't go negative if R_first_max8 is 0? The rule implies R_start=1 if they match, and R_start=R_first_max8-1 otherwise. If R_first_max8 is 0, and they don't match, R_first_any8 must be > 0, which is impossible. So R_first_max8 > 0 if they don't match. Let's clamp R_start just in case, though the logic suggests it might not be needed.
                R_start = max(0, R_start) # Clamp to 0 if R_first_max8 was 0 (though this case seems impossible based on logic)

            # Modify output grid from R_start downwards in C_target
            for r in range(R_start, num_rows):
                 # Check row bounds just in case, though range handles upper bound
                 if 0 <= r < num_rows:
                     output_grid[r][C_target] = 5
                     
    else:
        # Case 2: '8' is NOT present, check for '2'
        locations_2 = _find_digit_locations(input_grid, 2)
        
        if locations_2:
            # Find R_last2: maximum row index of any '2'
            R_last2 = -1
            for r, c in locations_2:
                if r > R_last2:
                    R_last2 = r
            
            # Find C_2: column index of '2' in row R_last2 
            # (assuming only one '2' in that row, or taking the first one found)
            C_2 = -1
            for r, c in locations_2:
                if r == R_last2:
                    C_2 = c
                    break # Take the first one found in that row
            
            if R_last2 != -1 and C_2 != -1:
                # Calculate C_target
                C_target = C_2 + 2
                
                # Modify the single cell if C_target is within bounds
                if 0 <= R_last2 < num_rows and 0 <= C_target < num_cols:
                    output_grid[R_last2][C_target] = 5

    # If neither '8' nor '2' was found, output_grid remains the initial copy
    return output_grid