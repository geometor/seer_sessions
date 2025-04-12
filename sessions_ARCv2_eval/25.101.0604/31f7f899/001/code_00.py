import copy

"""
Rule Description:

1.  Identify the horizontal 'axis' row in the input grid, which is the row containing the digit '6'. Let its index be `R`.
2.  Initialize the output grid with the same dimensions as the input, filled with the background digit '8'.
3.  Copy the axis row `R` from the input grid directly to the output grid at row `R`.
4.  For each cell `(r, c)` in the grid *not* on the axis row (`r != R`):
    a.  Determine the value on the axis row in the same column: `val_axis = input_grid[R][c]`.
    b.  If `val_axis` is '6', the output cell `output_grid[r][c]` remains '8'.
    c.  If `val_axis` is not '6', calculate the index of the symmetrically opposite row: `r_sym = R + (R - r)`.
    d.  Check if `r_sym` is a valid row index within the grid boundaries.
    e.  If `r_sym` is valid, get the value from the input grid at the symmetric position: `val_sym = input_grid[r_sym][c]`.
    f.  Compare the symmetric value `val_sym` with the axis value `val_axis`.
    g.  If `val_sym == val_axis`, then set the output cell `output_grid[r][c]` to `val_axis`.
    h.  If `r_sym` is invalid or if `val_sym != val_axis`, the output cell `output_grid[r][c]` remains '8'.
"""

def find_axis_row(grid: list[list[int]]) -> int:
    """Finds the index of the row containing the digit 6."""
    for r, row in enumerate(grid):
        if 6 in row:
            return r
    # Should not happen based on problem description/examples
    return -1 

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on reflection across an axis row
    and a matching condition with the symmetrically opposite cell.
    """
    
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Find the axis row index
    axis_row_index = find_axis_row(input_grid)
    if axis_row_index == -1:
         # Fallback or error handling if no axis row found
         # Based on examples, axis always exists.
         # Returning a copy or raising error might be options.
         # For now, assume it exists per problem structure.
         pass 

    # Initialize output_grid with background color 8
    output_grid = [[8 for _ in range(width)] for _ in range(height)]

    # Copy the axis row directly
    if 0 <= axis_row_index < height:
        output_grid[axis_row_index] = copy.deepcopy(input_grid[axis_row_index])

    # Iterate through each cell not on the axis row
    for r in range(height):
        if r == axis_row_index:
            continue

        for c in range(width):
            # Get the value from the axis row at this column
            val_axis = input_grid[axis_row_index][c]

            # If axis value is 6, output remains 8 (already initialized)
            if val_axis == 6:
                continue

            # Calculate symmetric row index
            r_sym = axis_row_index + (axis_row_index - r)

            # Check if symmetric row is within bounds
            if 0 <= r_sym < height:
                # Get value from symmetric position in input grid
                val_sym = input_grid[r_sym][c]

                # Condition: If symmetric value matches axis value
                if val_sym == val_axis:
                    # Set output cell to the axis value
                    output_grid[r][c] = val_axis
            # Else (r_sym out of bounds or val_sym != val_axis), 
            # output remains 8 (already initialized)

    return output_grid
