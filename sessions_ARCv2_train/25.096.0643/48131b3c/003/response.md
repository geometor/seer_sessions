```python
import copy
import numpy as np

"""
Transforms an input grid (N rows, M columns) containing a background color (0) and a single foreground color.
The transformation involves creating an intermediate grid (T) and then tiling it 2x2 to form the output grid (2N rows, 2M columns).

Steps:
1. Identify the unique non-zero foreground color in the input grid.
2. Create an intermediate grid T (N x M) based on the input:
   - If N < 2, T is a copy of the input.
   - If N >= 2:
     - Row 1 of T is a copy of Row 2 of the input.
     - Row 2 of T is a copy of Row 1 of the input.
     - For rows 3 to N of the input:
       - Create the corresponding row in T by swapping the background color (0) and the foreground color.
3. Create the final output grid (2N x 2M).
4. Tile the intermediate grid T into the output grid in a 2x2 pattern.
"""

def find_foreground_color(grid: list[list[int]]) -> int | None:
    """Finds the unique non-zero color in the grid."""
    foreground_color = None
    for row in grid:
        for cell in row:
            if cell != 0:
                if foreground_color is None:
                    foreground_color = cell
                elif foreground_color != cell:
                    # This case shouldn't happen based on the problem description,
                    # but good to acknowledge.
                    # We'll just proceed with the first one found.
                    return foreground_color
        if foreground_color is not None:
             # Optimization: stop searching once found
             break
    # If grid was all zeros, return 0 or a default. Based on examples,
    # a foreground color seems guaranteed if grid is non-empty.
    # If None is returned, it implies an all-zero grid or empty grid.
    return foreground_color

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation to the input grid.

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

    # --- Step 1: Identify Colors ---
    background_color = 0
    foreground_color = find_foreground_color(input_grid)
    # Handle case where grid might be all zeros
    if foreground_color is None:
        foreground_color = background_color # Treat as if background is the only color

    # --- Step 2: Create Intermediate Grid T ---
    intermediate_grid = [[0] * num_cols for _ in range(num_rows)]

    # Populate T based on input_grid rows
    if num_rows == 1:
        # Only one row, copy it directly
        intermediate_grid[0] = copy.deepcopy(input_grid[0])
    elif num_rows >= 2:
        # Swap first two rows
        intermediate_grid[0] = copy.deepcopy(input_grid[1])
        intermediate_grid[1] = copy.deepcopy(input_grid[0])

        # Process remaining rows (index 2 onwards, corresponding to input rows 3 onwards)
        for r in range(2, num_rows):
            input_row = input_grid[r]
            transformed_row = []
            for cell in input_row:
                if cell == background_color:
                    transformed_row.append(foreground_color)
                elif cell == foreground_color:
                    transformed_row.append(background_color)
                else:
                     # Should not happen with only two colors, but default to original
                    transformed_row.append(cell)
            intermediate_grid[r] = transformed_row

    # --- Step 3 & 4: Create Output Grid and Tile T ---
    output_num_rows = num_rows * 2
    output_num_cols = num_cols * 2
    output_grid = [[0] * output_num_cols for _ in range(output_num_rows)]

    # Fill the output grid by tiling the intermediate grid
    for r in range(output_num_rows):
        for c in range(output_num_cols):
            # Determine the corresponding row and column in the intermediate grid
            source_row = r % num_rows
            source_col = c % num_cols

            # Assign the value from the intermediate grid to the output grid cell
            output_grid[r][c] = intermediate_grid[source_row][source_col]

    return output_grid
```