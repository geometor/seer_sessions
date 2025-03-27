"""
The transformation extracts non-consecutively repeating rows from the input grid to create the output grid.
"""

def transform(input_grid):
    """
    Transforms an input grid by extracting unique, non-consecutively repeating rows.

    Args:
        input_grid: A list of lists representing the input grid,
                     where each inner list is a row of integers.

    Returns:
        A list of lists representing the output grid, formed by
        selecting unique rows from the input.
    """
    output_rows = []
    # Iterate through the rows of the input grid.
    for i in range(len(input_grid)):
        # If it's the first row, or if it's different from the previous row,
        # add it to the output rows.
        if i == 0 or input_grid[i] != input_grid[i-1]:
            output_rows.append(input_grid[i])
    return output_rows