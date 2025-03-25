```python
"""
Iterates through the input grid, examining vertical pairs of cells. 
If a specific color is found in the bottom cell of a vertical pair, 
the color of the top cell is replaced with the color of the bottom cell.
"""

import numpy as np

def get_vertical_pairs(grid):
    """Extracts all vertically adjacent pairs of cells."""
    pairs = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols):
            pairs.append( ((r, c), (r + 1, c)) )
    return pairs

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # get all vertical pairs
    pairs = get_vertical_pairs(input_grid)

    # loop through pairs for replacement
    for (top_row, top_col), (bottom_row, bottom_col) in pairs:
        top_color = input_grid[top_row, top_col]
        bottom_color = input_grid[bottom_row, bottom_col]

        # change output pixels
        if top_color != bottom_color:
            output_grid[top_row, top_col] = bottom_color


    return output_grid
```