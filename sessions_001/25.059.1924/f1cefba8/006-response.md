# f1cefba8 • 006 • refine_coder

---
```python
"""
The transformation involves identifying a rectangular block of red pixels enclosed by an azure border.
A new row is added above and below this block. All pixels within this expanded area, including the new rows, 
are set to red, except for the azure border itself. Finally, red pixels are added to the four corners 
of the expanded azure border, creating corner extensions.
"""

import numpy as np

def get_inner_block_coords(grid, border_color):
    """Finds the coordinates of the inner block surrounded by a border."""
    rows, cols = grid.shape
    
    # Find top-left corner
    top_row, left_col = -1, -1
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == border_color:
                if (r+1 < rows and c+1 < cols and
                    np.any(grid[r+1,c] != border_color) and np.any(grid[r,c+1] != border_color) ):

                    top_row, left_col = r+1, c+1
                    break
        if top_row != -1:
            break

    # Find bottom-right corner
    bottom_row, right_col = -1, -1
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
           if grid[r, c] == border_color:
                if (r-1 > 0 and c-1 > 0 and
                    np.any(grid[r-1,c] != border_color) and np.any(grid[r,c-1] != border_color) ):
                    bottom_row, right_col = r-1, c-1
                    break
        if bottom_row != -1:
            break

    return top_row, left_col, bottom_row, right_col

def transform(input_grid):
    """Transforms the input grid by adding rows and filling the inner block."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Boundaries (using azure border color)
    azure_color = 8
    red_color = 2
    top_row, left_col, bottom_row, right_col = get_inner_block_coords(input_grid, azure_color)
  
    # 2. Add new rows above and below
    output_grid = np.insert(output_grid, top_row, values=azure_color, axis=0)
    output_grid = np.insert(output_grid, bottom_row + 2, values=azure_color, axis=0) # +2 because of the inserted top row
    
    # Update coordinates
    top_row, left_col, bottom_row, right_col = get_inner_block_coords(output_grid, azure_color)

    # 3. Fill expanded area with red.
    for r in range(top_row - 1, bottom_row + 2):
        for c in range(left_col-1, right_col+2):
            if output_grid[r,c] == azure_color:
                if (r== top_row - 1 or r == bottom_row + 1 ) and ( c == left_col - 1 or c == right_col + 1 ): # corners
                    output_grid[r,c] = red_color
            else:
                output_grid[r, c] = red_color


    return output_grid
```
