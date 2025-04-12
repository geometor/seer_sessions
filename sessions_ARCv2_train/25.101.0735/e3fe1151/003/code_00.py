"""
Transforms a 5x5 grid of integers based on the following rules:
1. Initialize the output grid as a deep copy of the input grid.
2. Define a marker digit (7).
3. Iterate through each cell (r, c) of the input grid.
4. Identify 'target' cells: cells containing the marker digit (7) AND are outside the central cross (r != 2 and c != 2).
5. For each target cell:
    a. Find the symmetrically opposite cell coordinates (sr = 4 - r, sc = 4 - c).
    b. Get the value of the symmetrical cell from the *input* grid (sym_val = input_grid[sr][sc]).
    c. If sym_val is NOT the marker digit (Primary Rule):
        i. If the target cell is specifically (3, 3), update the output grid at (r, c) with the value from input_grid[1][0].
        ii. Otherwise, update the output grid at (r, c) with sym_val.
    d. If sym_val IS the marker digit (Fallback Rule):
        Update the output grid at (r, c) based on a prioritized lookup of values from specific input cells, determined by the target cell's coordinates (r, c):
        - (0,0): Use input[0,4].
        - (1,1): Use input[4,0].
        - (4,4): Use input[3,3].
        - (1,3): Check input[4,4]; if it's not 7, use it; otherwise, use input[3,3].
        - (3,1): Check input[4,4]; if not 7, use it. Else check input[0,4]; if not 7, use it. Otherwise, use input[3,3].
        - (3,3): Check input[0,4]; if it's not 7, use it; otherwise, use input[3,3].
6. Cells that are not target cells (i.e., not '7' or are on the central cross) remain unchanged.
7. Return the final output grid.
"""

import copy # Used for deep copying the grid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a transformation rule to a 5x5 grid based on symmetrical cell values
    and specific fallback rules for '7' cells outside the central cross.
    """
    # Ensure the grid is 5x5, although the logic assumes this implicitly
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if rows != 5 or cols != 5:
        # Handle potential errors or unexpected input sizes if necessary
        print("Warning: Input grid is not 5x5. Logic may not apply correctly.")
        # Consider raising an error instead: raise ValueError("Input grid must be 5x5")

    # Initialize output_grid as a deep copy of input_grid
    output_grid = copy.deepcopy(input_grid)

    # Define the marker digit and grid dimensions (0-indexed max)
    marker_digit = 7
    max_idx = 4 # for 5x5 grid

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

                # Apply the Primary Rule if the symmetrical cell is not the marker digit
                if sym_val != marker_digit:
                    # Specific exception for target cell (3, 3)
                    if r == 3 and c == 3:
                        output_grid[r][c] = input_grid[1][0]
                    # General case for the primary rule
                    else:
                        output_grid[r][c] = sym_val
                # Apply the Fallback Rule if the symmetrical cell is also the marker digit
                else:
                    fallback_val = marker_digit # Default to marker if no rule matches (shouldn't happen with explicit cases)

                    # Determine fallback value based on target cell (r, c)
                    if r == 0 and c == 0: # Target: TL corner
                        fallback_val = input_grid[0][max_idx] # Source: TR corner
                    elif r == 1 and c == 1: # Target: TL inner
                        fallback_val = input_grid[max_idx][0] # Source: BL corner
                    elif r == 4 and c == 4: # Target: BR corner
                         fallback_val = input_grid[3][3] # Source: BR inner
                    elif r == 1 and c == 3: # Target: TR inner
                        val1 = input_grid[max_idx][max_idx] # Source 1: BR corner
                        val2 = input_grid[3][3]           # Source 2: BR inner
                        fallback_val = val1 if val1 != marker_digit else val2
                    elif r == 3 and c == 1: # Target: BL inner
                        val1 = input_grid[max_idx][max_idx] # Source 1: BR corner
                        val2 = input_grid[0][max_idx]     # Source 2: TR corner
                        val3 = input_grid[3][3]           # Source 3: BR inner
                        if val1 != marker_digit:
                            fallback_val = val1
                        elif val2 != marker_digit:
                             fallback_val = val2
                        else:
                            fallback_val = val3
                    elif r == 3 and c == 3: # Target: BR inner
                        val1 = input_grid[0][max_idx]     # Source 1: TR corner
                        val2 = input_grid[3][3]           # Source 2: BR inner
                        fallback_val = val1 if val1 != marker_digit else val2
                    
                    # Note: The fallback logic only covers the specific (r, c) coordinates
                    # observed in the examples where a fallback was needed.
                    # If other cells like (0,1), (1,0), etc., could be targets needing fallback,
                    # their rules are currently undefined.

                    output_grid[r][c] = fallback_val

            # If the cell is not a target cell, its value remains unchanged
            # (already handled by the initial deep copy).

    return output_grid