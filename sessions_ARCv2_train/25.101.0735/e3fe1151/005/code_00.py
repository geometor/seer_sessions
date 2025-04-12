"""
Transforms a 5x5 grid of integers based on the following rules:
1. Initialize the output grid as a deep copy of the input grid.
2. Define a marker digit M = 7 and grid max index max_idx = 4.
3. Iterate through each cell (r, c) of the input grid.
4. Skip cells that are inside the central cross (r == 2 or c == 2) or do not contain the marker digit.
5. For the remaining 'target' cells (value is M, outside the cross):
    a. Find the symmetrically opposite cell coordinates (sr = 4 - r, sc = 4 - c) and its value (sym_val = input_grid[sr][sc]).
    b. If sym_val is NOT M (Primary Rule):
        i. If the target cell is (3, 3), set output_grid[r][c] = input_grid[1][0].
        ii. Otherwise, set output_grid[r][c] = sym_val.
    c. If sym_val IS M (Fallback Rule):
        Determine the replacement value 'fallback_val' based on the target cell's coordinates (r,c):
        - (0,0): Use input_grid[0][4].
        - (1,1): Use input_grid[4][0].
        - (1,3): Check input_grid[4][4]; if not M, use it; otherwise use input_grid[3][3].
        - (3,1): SPECIAL CASE: Check input_grid[1][0]. If not 0, use it. Otherwise (if input_grid[1][0] is 0), perform a priority check: use input_grid[4][4] if not M; else use input_grid[0][4] if not M; else use input_grid[3][3].
        - (3,3): Check input_grid[0][4]; if not M, use it; otherwise use input_grid[3][3].
        - (4,4): Use input_grid[3][3].
        Set output_grid[r][c] = fallback_val.
6. Return the final output grid.
"""

import copy # Used for deep copying the grid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies transformation rules to a 5x5 grid, focusing on cells with value 7
    outside the central cross, using symmetric values and complex fallback rules.
    """
    # Basic validation and setup
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if rows != 5 or cols != 5:
        # Consider raising an error for invalid input size
        raise ValueError("Input grid must be 5x5")

    # Initialize output_grid as a deep copy of input_grid
    output_grid = copy.deepcopy(input_grid)

    # Define constants
    marker_digit = 7
    max_idx = 4 # Grid size 5 -> max index 4

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the cell should be skipped (invariant)
            # Skip if it's on the central cross (r=2 or c=2)
            # Skip if it doesn't contain the marker digit
            if r == 2 or c == 2 or input_grid[r][c] != marker_digit:
                continue # Value remains unchanged from the initial copy

            # --- Cell (r, c) is a target cell ---
            # Calculate symmetric coordinates and value
            sr = max_idx - r
            sc = max_idx - c
            sym_val = input_grid[sr][sc]

            # Apply Primary Rule (symmetric cell is NOT the marker digit)
            if sym_val != marker_digit:
                # Specific exception for target cell (3, 3)
                if r == 3 and c == 3:
                    output_grid[r][c] = input_grid[1][0] # Use value from (1,0)
                # General case for the primary rule
                else:
                    output_grid[r][c] = sym_val # Use symmetric value

            # Apply Fallback Rule (symmetric cell IS the marker digit)
            else:
                fallback_val = marker_digit # Default value (should be overwritten)

                # Determine fallback value based on target cell (r, c)
                if r == 0 and c == 0: # Target: TL corner
                    fallback_val = input_grid[0][max_idx] # Source: TR corner

                elif r == 1 and c == 1: # Target: TL inner
                    fallback_val = input_grid[max_idx][0] # Source: BL corner

                elif r == 1 and c == 3: # Target: TR inner
                    val1 = input_grid[max_idx][max_idx] # Source 1: BR corner
                    val2 = input_grid[3][3]           # Source 2: BR inner
                    # Use val1 if it's not the marker, otherwise use val2
                    fallback_val = val1 if val1 != marker_digit else val2

                elif r == 3 and c == 1: # Target: BL inner - Special Case
                    neighbor_val = input_grid[1][0] # Check inner-neighbor value
                    if neighbor_val != 0: # Use neighbor if it's not 0
                        fallback_val = neighbor_val
                    else: # If neighbor is 0, use priority check
                        val1 = input_grid[max_idx][max_idx] # Source 1: BR corner
                        val2 = input_grid[0][max_idx]     # Source 2: TR corner
                        val3 = input_grid[3][3]           # Source 3: BR inner
                        if val1 != marker_digit:
                            fallback_val = val1
                        elif val2 != marker_digit:
                            fallback_val = val2
                        else:
                            fallback_val = val3 # Use val3 if val1 and val2 are markers

                elif r == 3 and c == 3: # Target: BR inner
                    val1 = input_grid[0][max_idx]     # Source 1: TR corner
                    val2 = input_grid[3][3]           # Source 2: BR inner
                    # Use val1 if it's not the marker, otherwise use val2
                    fallback_val = val1 if val1 != marker_digit else val2

                elif r == 4 and c == 4: # Target: BR corner
                    fallback_val = input_grid[3][3] # Source: BR inner

                # Assign the determined fallback value to the output grid
                output_grid[r][c] = fallback_val

    # Return the transformed grid
    return output_grid