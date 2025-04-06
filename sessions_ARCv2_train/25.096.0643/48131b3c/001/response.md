```python
import copy

"""
Transforms an input grid of integers (N rows, M columns) into an output grid (2N rows, 2M columns).
The transformation involves two steps:
1. Row Rearrangement: An intermediate grid is created by swapping the first two rows of the input grid. 
   If the input grid has fewer than two rows, the intermediate grid is identical to the input.
2. Tiling: The final output grid is constructed by tiling the intermediate grid in a 2x2 pattern. 
   This means the intermediate grid is repeated twice horizontally and twice vertically.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the row swap and 2x2 tiling transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid of integers.

    Returns:
        A list of lists representing the transformed output grid.
    """

    # --- Step 0: Handle edge cases and get dimensions ---
    num_rows = len(input_grid)
    if num_rows == 0:
        return []  # Return empty list for empty input grid

    num_cols = len(input_grid[0]) if num_rows > 0 else 0
    if num_cols == 0:
         # Return a grid with doubled rows but still zero columns
        return [[] for _ in range(num_rows * 2)]

    # --- Step 1: Row Rearrangement (Create Intermediate Grid) ---
    # Create a deep copy to avoid modifying the original input grid
    intermediate_grid = copy.deepcopy(input_grid)

    # Swap the first two rows if the grid has at least two rows
    if num_rows >= 2:
        intermediate_grid[0], intermediate_grid[1] = intermediate_grid[1], intermediate_grid[0]
        
    # --- Step 2: Tiling (Create Output Grid) ---
    # Calculate output dimensions
    output_num_rows = num_rows * 2
    output_num_cols = num_cols * 2

    # Initialize the output grid (e.g., with zeros, will be overwritten)
    output_grid = [[0] * output_num_cols for _ in range(output_num_rows)]

    # Fill the output grid by tiling the intermediate grid
    for r in range(output_num_rows):
        for c in range(output_num_cols):
            # Determine the corresponding row and column in the intermediate grid
            # Use the modulo operator to wrap around the dimensions of the intermediate grid
            source_row = r % num_rows
            source_col = c % num_cols

            # Assign the value from the intermediate grid to the output grid cell
            output_grid[r][c] = intermediate_grid[source_row][source_col]

    return output_grid
```