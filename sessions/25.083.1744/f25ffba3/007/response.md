```python
"""
1. Find the bottom-most 1x4 horizontal block containing four distinct non-zero colors.
2. Copy the input to the output.
3. Overwrite the first row of the output grid with the colors of the found block.
"""

import numpy as np

def find_colored_block(grid):
    """Finds the bottom-most 1x4 horizontal block with four distinct non-zero colors."""
    rows, cols = grid.shape
    for r in range(rows - 1, -1, -1):  # Iterate upwards from the bottom
        for c in range(cols - 3):
            colors = grid[r, c:c+4]
            if len(set(colors)) == 4 and all(color != 0 for color in colors):  # Four unique non-zero colors
                return r, c, colors
    return None, None, None

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Initialize output_grid with the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the 1x4 block (bottom-most)
    start_row, start_col, colors = find_colored_block(input_grid)
    if start_row is None:
        return output_grid  # Return input grid if no block is found

    # Overwrite the first row of the output grid with the colors of the block
    output_grid[0, :min(4,cols)] = colors[:min(4,cols)] # handles edge cases

    return output_grid
```