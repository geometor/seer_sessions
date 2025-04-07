```python
import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on column content and then tiles the result.

    1. Creates an intermediate grid of the same dimensions as the input.
    2. For each column in the input grid:
        a. If the column contains any non-zero value, copy non-zero values
           to the intermediate grid's corresponding column and replace zeros
           with 8.
        b. If the column contains only zeros, copy the zeros to the
           intermediate grid's corresponding column.
    3. Creates an output grid twice the height and twice the width of the input.
    4. Tiles the intermediate grid into the output grid in a 2x2 pattern.
    """

    # Get input dimensions
    if not input_grid or not input_grid[0]:
        return []  # Handle empty input
    height = len(input_grid)
    width = len(input_grid[0])

    # --- Create Intermediate Grid ---

    # Initialize intermediate_grid with zeros
    intermediate_grid = [[0 for _ in range(width)] for _ in range(height)]

    # Iterate through each column of the input grid
    for j in range(width):
        # Check if the current column contains any non-zero value
        contains_non_zero = False
        for i in range(height):
            if input_grid[i][j] != 0:
                contains_non_zero = True
                break

        # Populate the corresponding column in the intermediate grid
        for i in range(height):
            if contains_non_zero:
                # If column has non-zeros, replace 0s with 8s, keep non-zeros
                if input_grid[i][j] == 0:
                    intermediate_grid[i][j] = 8
                else:
                    intermediate_grid[i][j] = input_grid[i][j]
            else:
                # If column has only zeros, keep them as 0 (already initialized)
                intermediate_grid[i][j] = 0 # Explicit assignment

    # --- Create Output Grid by Tiling ---

    # Calculate output dimensions
    output_height = 2 * height
    output_width = 2 * width

    # Initialize output_grid
    output_grid = [[0 for _ in range(output_width)] for _ in range(output_height)]

    # Tile the intermediate_grid into the output_grid
    for r in range(output_height):
        for c in range(output_width):
            # Determine the corresponding row and column in the intermediate grid
            intermediate_row = r % height
            intermediate_col = c % width
            # Assign the value from the intermediate grid
            output_grid[r][c] = intermediate_grid[intermediate_row][intermediate_col]

    return output_grid
```