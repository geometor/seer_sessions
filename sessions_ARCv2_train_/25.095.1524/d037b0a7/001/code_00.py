import copy

"""
Transforms an input grid based on a vertical downward filling rule.
Non-zero values in the input grid are copied to the output grid.
Zero values in the input grid are replaced in the output grid by the value 
of the nearest non-zero cell directly above them in the same column of the input grid. 
If all cells above a zero cell in the input grid are also zero, the output cell remains zero.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a vertical downward fill transformation to the input grid.

    Args:
        input_grid: A list of lists representing the 2D input grid of integers.

    Returns:
        A list of lists representing the transformed 2D output grid.
    """
    # Ensure input_grid is not empty to avoid index errors
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize output_grid with zeros, same dimensions as input_grid
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Iterate through each column
    for c in range(cols):
        # Iterate through each row within the column
        for r in range(rows):
            # Get the value from the input grid
            input_value = input_grid[r][c]

            # If the input value is non-zero, copy it directly to the output
            if input_value != 0:
                output_grid[r][c] = input_value
            # If the input value is zero, look upwards in the input grid
            else:
                # Start searching from the row directly above (r-1) up to row 0
                found_value = 0 # Default to 0 if no non-zero is found above
                for r_source in range(r - 1, -1, -1):
                    # Check the value in the input grid above the current cell
                    value_above = input_grid[r_source][c]
                    # If a non-zero value is found
                    if value_above != 0:
                        # Assign this value to the output grid and stop searching upwards
                        found_value = value_above
                        break 
                # Assign the found value (or 0 if none was found) to the output cell
                output_grid[r][c] = found_value

    return output_grid