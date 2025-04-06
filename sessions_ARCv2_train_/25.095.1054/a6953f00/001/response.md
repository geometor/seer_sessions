```python
import math

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms an input grid of integers into a 2x2 output grid.
    The transformation rule depends on the parity of the number of columns (C)
    in the input grid:
    - If C is odd, the output is the top-left 2x2 subgrid.
    - If C is even, the output is the top-right 2x2 subgrid.
    """

    # Determine the number of columns in the input grid
    if not input_grid or not input_grid[0]:
        # Handle empty or invalid input if necessary
        return [] 
    num_columns = len(input_grid[0])

    # Initialize the output grid (will be 2x2)
    output_grid = [[0, 0], [0, 0]]

    # Check the parity of the number of columns
    if num_columns % 2 != 0:  # Odd number of columns
        # Extract the top-left 2x2 subgrid
        # Ensure the grid is at least 2x2
        if len(input_grid) >= 2 and num_columns >= 2:
            output_grid[0][0] = input_grid[0][0]
            output_grid[0][1] = input_grid[0][1]
            output_grid[1][0] = input_grid[1][0]
            output_grid[1][1] = input_grid[1][1]
        else:
             # Handle cases where the grid is too small for the required extraction
             # Depending on requirements, might return empty, raise error, or partial grid
             # For now, returning the initialized (potentially incorrect) grid or an empty one
             return [] # Or raise ValueError("Input grid too small")
            
    else:  # Even number of columns
        # Extract the top-right 2x2 subgrid
        # Ensure the grid is at least 2x2
        if len(input_grid) >= 2 and num_columns >= 2:
            start_col_index = num_columns - 2
            output_grid[0][0] = input_grid[0][start_col_index]
            output_grid[0][1] = input_grid[0][start_col_index + 1]
            output_grid[1][0] = input_grid[1][start_col_index]
            output_grid[1][1] = input_grid[1][start_col_index + 1]
        else:
             # Handle cases where the grid is too small
             return [] # Or raise ValueError("Input grid too small")

    return output_grid
```