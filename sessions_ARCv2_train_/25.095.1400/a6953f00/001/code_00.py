import math

"""
Transforms an input square grid of integers into a 2x2 output grid.
The transformation rule depends on the parity of the input grid's dimensions:
- If the dimension (number of rows/columns) is even, the output is the top-right 2x2 subgrid.
- If the dimension is odd, the output is the top-left 2x2 subgrid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Extracts a 2x2 subgrid from the input grid based on the parity of its dimensions.

    Args:
        input_grid: A square list of lists representing the input grid of integers.

    Returns:
        A 2x2 list of lists representing the extracted subgrid.
    """

    # Get the dimensions of the input grid (assuming it's square)
    n = len(input_grid)

    # Determine the starting row and column for the 2x2 subgrid
    if n % 2 == 0:
        # Even dimension: select top-right 2x2 subgrid
        start_row = 0
        start_col = n - 2
    else:
        # Odd dimension: select top-left 2x2 subgrid
        start_row = 0
        start_col = 0

    # Initialize the output grid
    output_grid = []

    # Extract the 2x2 subgrid
    # Iterate through the rows of the subgrid (0 and 1 relative to start_row)
    for i in range(2):
        # Get the current row from the input grid based on start_row
        input_row = input_grid[start_row + i]
        # Slice the row to get the columns for the subgrid based on start_col
        output_row = input_row[start_col : start_col + 2]
        # Append the extracted row to the output grid
        output_grid.append(output_row)

    # Return the extracted 2x2 subgrid
    return output_grid