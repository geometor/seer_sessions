import copy

"""
Transforms a 5x5 grid of digits based on the following rules:
1. Initialize the output grid as a copy of the input grid.
2. Identify the central cross (row index 2 or column index 2) and cells outside the cross whose value is not 7. These cells remain unchanged.
3. Iterate through each remaining cell (r, c) (where r!=2, c!=2, and input_grid[r][c] == 7).
4. For each such cell:
   a. Determine its quadrant (UL, UR, LL, LR) relative to the central cross.
   b. Define primary and alternate source cells based on the quadrant:
      - LR quadrant (r > 2, c > 2): Primary source is (0, 4), Alternate is (4, 4).
      - UL, UR, LL quadrants: Primary source is (4, 4), Alternate is (0, 4).
   c. Get the values v_p and v_a from the primary and alternate source cells in the *input* grid.
   d. Determine the replacement value: If v_p is not 7, use v_p. Otherwise, use v_a.
   e. Update the output grid cell (r, c) with the replacement value.
5. Return the modified output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a quadrant-based transformation rule to '7's outside the central cross.
    """
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0]) # Assuming 5x5

    # Define source cell coordinates
    # Top-Right corner (used as primary for LR, alternate for others)
    source_tr = (0, 4)
    # Bottom-Right corner (used as primary for UL/UR/LL, alternate for LR)
    source_br = (4, 4)

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Rule 2: Skip cells in the central cross (row 2 or column 2)
            if r == 2 or c == 2:
                continue

            # Rule 2: Skip cells outside the cross that are not 7
            if input_grid[r][c] != 7:
                continue

            # Rule 3 & 4: Process cells where r!=2, c!=2, and input_grid[r][c] == 7
            
            # 4a: Determine quadrant
            is_lr_quadrant = (r > 2 and c > 2)

            # 4b: Identify primary and alternate source coordinates
            if is_lr_quadrant:
                primary_source_coord = source_tr
                alternate_source_coord = source_br
            else: # UL, UR, or LL quadrant
                primary_source_coord = source_br
                alternate_source_coord = source_tr

            # 4c: Get source values from the *input* grid
            v_p = input_grid[primary_source_coord[0]][primary_source_coord[1]]
            v_a = input_grid[alternate_source_coord[0]][alternate_source_coord[1]]

            # 4d: Determine replacement value
            replacement_value = v_p if v_p != 7 else v_a

            # 4e: Update the output grid
            output_grid[r][c] = replacement_value

    # 5: Return the final output grid
    return output_grid
