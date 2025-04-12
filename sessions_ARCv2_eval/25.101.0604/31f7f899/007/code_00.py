"""
The transformation identifies a horizontal 'axis' row in the input grid (the row containing '6'). 
The output grid is initialized with a background color ('8'). The axis row itself is copied directly from the input to the output.
For all other cells (r, c) not on the axis row:
1. The axis value (val_axis) at input[R][c] is checked. If it's '6', the output remains '8'.
2. The symmetric row index (r_sym) is calculated. If it's out of bounds, the output remains '8'.
3. The original value (val_orig = input[r][c]) and symmetric value (val_sym = input[r_sym][c]) are retrieved.
4. The output cell output[r][c] is set to val_axis if ANY of the following four conditions are met:
    a) val_orig is background (8) AND val_sym is background (8).
    b) val_orig is background (8) AND val_sym matches val_axis.
    c) val_orig matches val_axis AND val_sym is background (8).
    d) val_orig matches val_axis AND val_sym matches val_axis AND the current row 'r' is adjacent to the axis row R (abs(r - R) == 1).
5. If none of these conditions are met, the output cell remains background '8'.
"""

import copy

def find_axis_row(grid: list[list[int]], height: int) -> int:
    """Finds the index of the row containing the digit 6."""
    for r in range(height):
        # Check if row exists and contains 6
        if 6 in grid[r]:
            return r
    # Axis row is expected based on examples
    return -1 

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Transforms the input grid based on symmetric reflection across an axis row,
    applying specific conditions based on original, symmetric, and axis values.
    """
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Find the axis row index (row containing 6)
    axis_row_index = find_axis_row(input_grid, height)
    
    # Axis row must exist based on problem description
    if axis_row_index == -1:
         # Handle error: This case should not occur based on examples
         print("Error: Axis row containing '6' not found.")
         # Return a copy or raise an error, returning copy for now
         return copy.deepcopy(input_grid) 

    # Initialize output_grid with background color 8
    output_grid = [[8 for _ in range(width)] for _ in range(height)]

    # Copy the axis row directly from input to output
    output_grid[axis_row_index] = copy.deepcopy(input_grid[axis_row_index])

    # Iterate through each cell not on the axis row
    for r in range(height):
        if r == axis_row_index:
            continue # Skip the axis row itself

        for c in range(width):
            # Get the value from the axis row at this column
            val_axis = input_grid[axis_row_index][c]

            # If axis value is 6, output remains 8 (already initialized). Skip.
            if val_axis == 6:
                continue

            # Calculate symmetric row index
            r_sym = axis_row_index + (axis_row_index - r)

            # Check if symmetric row is within bounds. If not, output remains 8. Skip.
            if not (0 <= r_sym < height):
                continue

            # Get value from original position in input grid
            val_orig = input_grid[r][c]
            # Get value from symmetric position in input grid
            val_sym = input_grid[r_sym][c]

            # Check the four conditions to determine if output should be val_axis
            # Condition 1: Original is background AND Symmetric is background
            cond1 = (val_orig == 8 and val_sym == 8)
            # Condition 2: Original is background AND Symmetric matches axis
            cond2 = (val_orig == 8 and val_sym == val_axis)
            # Condition 3: Original matches axis AND Symmetric is background
            cond3 = (val_orig == val_axis and val_sym == 8)
            # Condition 4: Original matches axis AND Symmetric matches axis AND Row is adjacent to axis
            is_adjacent = abs(r - axis_row_index) == 1
            cond4 = (val_orig == val_axis and val_sym == val_axis and is_adjacent)

            # If any condition is true, set output cell to the axis value
            if cond1 or cond2 or cond3 or cond4:
                output_grid[r][c] = val_axis
            # Else: output remains 8 (already initialized)

    return output_grid