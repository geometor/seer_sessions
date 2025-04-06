"""
Transforms an input 2D grid of integers into an output grid based on the following rule:
Iterate through each row of the input grid. For each row, identify the value in the first column (column index 0). This value becomes the 'replacement value' for that specific row. Then, iterate through all cells in that row. If a cell contains the value 5, replace it with the 'replacement value' determined for that row. If a cell contains any value other than 5, keep its original value. The output grid has the same dimensions as the input grid.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the 2D input grid of integers.

    Returns:
        A list of lists representing the 2D output grid after transformation.
    """
    # Initialize output_grid as a deep copy of the input to preserve original non-5 values
    # and dimensions easily.
    output_grid = copy.deepcopy(input_grid)
    
    # Get the dimensions of the grid
    num_rows = len(input_grid)
    if num_rows == 0:
        return [] # Handle empty grid case
    num_cols = len(input_grid[0])
    if num_cols == 0:
        return [[] for _ in range(num_rows)] # Handle case with empty rows

    # Iterate through each row
    for r in range(num_rows):
        # Determine the replacement value for the current row (value in the first column)
        # Check if the row is not empty before accessing the first element
        if num_cols > 0:
            replacement_value = input_grid[r][0]
        else:
            continue # Skip empty rows

        # Iterate through each column in the current row
        for c in range(num_cols):
            # Check if the cell value in the input grid is 5
            if input_grid[r][c] == 5:
                # If it is 5, update the corresponding cell in the output grid
                # with the replacement value for this row.
                output_grid[r][c] = replacement_value
            # Else (if the value is not 5), the value from the initial deep copy is kept.

    # Return the modified grid
    return output_grid