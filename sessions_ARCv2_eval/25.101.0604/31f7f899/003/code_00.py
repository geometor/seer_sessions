import copy

"""
The transformation identifies a horizontal 'axis' row in the input grid, characterized by the presence of the digit '6'. 
The output grid is initialized with a background color ('8') and the axis row is copied directly from the input. 
For all other cells (r, c) not on the axis row, the output value is determined by comparing the input values at the cell's original position (r, c), 
its symmetrically opposite position (r_sym, c) relative to the axis row, and the axis value at the same column (R, c).
Specifically, the output cell output_grid[r][c] takes the value val_axis = input_grid[R][c] if:
1. val_axis is not '6'.
2. The symmetric row r_sym = R + (R - r) is within the grid bounds.
3. The value at the symmetric position val_sym = input_grid[r_sym][c] either matches the axis value (val_sym == val_axis) OR is the background color (val_sym == 8).
4. An exception case is NOT met: the exception occurs if both the original value val_orig = input_grid[r][c] and the symmetric value val_sym already match the axis value (val_orig == val_axis and val_sym == val_axis).
If the conditions are met and the exception does not apply, output_grid[r][c] becomes val_axis. Otherwise, it remains the background color '8'.
"""

def find_axis_row(grid: list[list[int]]) -> int:
    """Finds the index of the row containing the digit 6."""
    for r, row in enumerate(grid):
        if 6 in row:
            return r
    # This case should ideally not be reached based on problem constraints
    # If it could happen, raising an error or returning None might be better.
    return -1 

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Find the axis row index
    axis_row_index = find_axis_row(input_grid)
    # Assuming axis row always exists based on examples
    if axis_row_index == -1:
        # Handle error or return default if axis not found, though unexpected
        return copy.deepcopy(input_grid) # Or raise ValueError("Axis row not found")

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

            # If axis value is 6, output remains 8 (already initialized). Skip.
            if val_axis == 6:
                continue

            # Calculate symmetric row index
            r_sym = axis_row_index + (axis_row_index - r)

            # Check if symmetric row is within bounds
            if 0 <= r_sym < height:
                # Get value from symmetric position in input grid
                val_sym = input_grid[r_sym][c]
                # Get value from original position in input grid
                val_orig = input_grid[r][c]

                # Check if the reflection rule applies
                rule_applies = (val_sym == val_axis) or (val_sym == 8)
                
                # Check for the exception case
                is_exception = (val_orig == val_axis) and (val_sym == val_axis)

                # If the rule applies AND it's not the exception case, set output to axis value
                if rule_applies and not is_exception:
                    output_grid[r][c] = val_axis
                # Else (rule doesn't apply OR exception applies), output remains 8 (already initialized)

            # Else (r_sym out of bounds), output remains 8 (already initialized)

    return output_grid