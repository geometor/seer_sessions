```python
"""
Upscales an input grid by a factor of 3. Each cell in the input grid 
is expanded into a 3x3 block of the same value in the output grid.
The position of the input cell (r, c) determines the top-left corner 
(r * 3, c * 3) of the corresponding 3x3 block in the output grid.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms an input grid by expanding each cell into a 3x3 block 
    in the output grid.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the upscaled 3x3 output grid.
    """
    # Determine the dimensions of the input grid
    input_rows = len(input_grid)
    if input_rows == 0:
        return [] # Handle empty input grid
    input_cols = len(input_grid[0])
    if input_cols == 0:
        # Handle rows with no columns, though typically grid implies uniform columns
        return [[] for _ in range(input_rows * 3)] 

    # Calculate the dimensions of the output grid
    output_rows = input_rows * 3
    output_cols = input_cols * 3

    # Initialize the output grid with zeros (or any placeholder)
    # Using numpy for easier initialization and slicing, then convert back if needed
    output_grid_np = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through each cell of the input grid
    for r in range(input_rows):
        for c in range(input_cols):
            # Get the value from the input cell
            value = input_grid[r][c]

            # Determine the top-left corner of the 3x3 block in the output grid
            start_row = r * 3
            start_col = c * 3

            # Fill the corresponding 3x3 block in the output grid with the value
            # Using numpy slicing for efficiency
            output_grid_np[start_row:start_row + 3, start_col:start_col + 3] = value

    # Convert the numpy array back to a list of lists for the final output format
    output_grid = output_grid_np.tolist()

    return output_grid

```