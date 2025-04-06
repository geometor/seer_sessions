```python
import copy

"""
Transforms an input grid of digits based on the presence and location of '8's and '2's.

The rules are applied hierarchically:

1.  If the digit '8' is present:
    a.  Find the maximum column index (C_max8) where an '8' appears.
    b.  Calculate the target column (C_target = C_max8 + 2).
    c.  Find the minimum row index (R_first_any8) containing any '8'.
    d.  Find the minimum row index (R_first_max8) containing an '8' specifically in column C_max8.
    e.  If R_first_any8 equals R_first_max8:
        i.  If the digit '2' is also present:
            - Find the maximum row index (R_last2) containing a '2'.
            - Change only the cell at (R_last2, C_target) to '5'.
        ii. If the digit '2' is NOT present:
            - Set the starting row R_start = 1.
            - Change all cells in column C_target from row R_start downwards to '5'.
    f.  If R_first_any8 is NOT equal to R_first_max8:
        i.  Set the starting row R_start = R_first_max8 - 1 (clamped at 0).
        ii. Change all cells in column C_target from row R_start downwards to '5'.
2.  If the digit '8' is NOT present, but the digit '2' is present:
    a.  Find the maximum row index (R_last2) where a '2' appears.
    b.  Find the column index (C_last2) of the first '2' found in row R_last2.
    c.  Calculate the target column (C_target = C_last2 + 2).
    d.  Change only the cell at (R_last2, C_target) to '5'.
3.  If neither '8' nor '2' is present, the grid remains unchanged.

Boundary checks are performed to ensure modifications only happen within the grid dimensions.
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
        return copy.deepcopy(input_grid) # Return copy or empty list? Returning copy.

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
        
        # Calculate C_target from '8'
        C_target = C_max8 + 2

        # Check if C_target is within grid bounds
        if C_target < num_cols:
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

            # Rule 1.e: R_first_any8 == R_first_max8
            if R_first_any8 == R_first_max8:
                # Rule 1.e.i: '2' is also present
                if has_2:
                    # Find R_last2: maximum row index of any '2'
                    R_last2 = -1
                    for r, c in locations_2:
                        if r > R_last2:
                            R_last2 = r
                    # Modify the single cell at (R_last2, C_target) if R_last2 is valid
                    if R_last2 != -1 and 0 <= R_last2 < num_rows:
                         output_grid[R_last2][C_target] = 5
                # Rule 1.e.ii: '2' is NOT present
                else:
                    R_start = 1 # Start modifying from row 1
                    # Modify column C_target from R_start downwards
                    for r in range(R_start, num_rows):
                        output_grid[r][C_target] = 5
            # Rule 1.f: R_first_any8 != R_first_max8
            else:
                # Ensure R_first_max8 is valid before calculating R_start
                if R_first_max8 < num_rows: 
                   R_start = max(0, R_first_max8 - 1) # Start modifying from R_first_max8 - 1 (clamped at 0)
                   # Modify column C_target from R_start downwards
                   for r in range(R_start, num_rows):
                       output_grid[r][C_target] = 5

    # Rule 2: '8' is NOT present, but '2' IS present
    elif has_2:
        # Find R_last2: maximum row index of any '2'
        R_last2 = -1
        for r, c in locations_2:
            if r > R_last2:
                R_last2 = r
        
        # Find C_last2: column index of the first '2' in row R_last2 
        C_last2 = -1
        if R_last2 != -1:
            for r, c in locations_2:
                if r == R_last2:
                    C_last2 = c
                    break # Take the first one found in that row
        
        # Proceed if both R_last2 and C_last2 were found
        if R_last2 != -1 and C_last2 != -1:
            # Calculate C_target from '2'
            C_target = C_last2 + 2
            
            # Modify the single cell if C_target is within bounds
            if 0 <= R_last2 < num_rows and 0 <= C_target < num_cols:
                output_grid[R_last2][C_target] = 5

    # Rule 3: Neither '8' nor '2' is present - No changes needed, output_grid is already a copy

    return output_grid
```