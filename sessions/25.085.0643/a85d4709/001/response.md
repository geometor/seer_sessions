```python
"""
Transform an input grid where each row contains exactly one 'gray' (5) pixel.
The output grid has the same dimensions as the input.
Each row in the output grid is filled with a single color determined by the
column index of the 'gray' pixel in the corresponding input row:
- 'gray' in column 0 -> output row filled with 'red' (2).
- 'gray' in column 1 -> output row filled with 'yellow' (4).
- 'gray' in column 2 -> output row filled with 'green' (3).
"""

import copy

def transform(input_grid):
    """
    Transforms the input grid based on the column position of the 'gray' pixel in each row.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Get dimensions of the input grid
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Initialize output_grid as a deep copy of the input grid
    # We will overwrite the values row by row
    output_grid = [[0 for _ in range(width)] for _ in range(height)] # Initialize with 0s is clearer

    # Iterate through each row of the input grid
    for r in range(height):
        input_row = input_grid[r]
        fill_color = 0 # Default color, though problem implies a 5 is always present

        # Find the column index 'c' of the 'gray' (5) pixel in the current row
        try:
            c = input_row.index(5)

            # Determine the output color based on the column index 'c'
            if c == 0:
                fill_color = 2 # red
            elif c == 1:
                fill_color = 4 # yellow
            elif c == 2:
                fill_color = 3 # green
            # Note: If c > 2, fill_color remains 0 based on current logic,
            # but the examples only cover columns 0, 1, 2.
            # Assuming the pattern might not extend or needs clarification for wider grids.

        except ValueError:
            # Handle the case where 'gray' (5) is not found in the row,
            # although the problem description implies it's always present.
            # We'll leave the row as initialized (e.g., all 0s) or potentially raise an error.
            # For now, let's proceed assuming it's always found based on examples.
            pass # Keep fill_color as 0 or handle error as needed

        # Fill the corresponding output row entirely with the determined fill_color
        for col_index in range(width):
            output_grid[r][col_index] = fill_color

    return output_grid
```