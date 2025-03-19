# a78176bb • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify the Primary Diagonal:** Find the diagonal line of cells running from the top-left to the bottom-right of the input grid. Note the color of this diagonal.
2.  **Identify Secondary Diagonal:** Find the color used to draw the main diagonal. Draw a diagonal from top-right to bottom-left, only on the cells that are 0 (white).
3.  **Identify the Block:** Locate any contiguous block of cells of a color different from the diagonal color and from white (0).
4.  **Remove the Block:** Set the values of all cells within the identified block to 0 (white).
5. **Construct Output.** The output is composed by the two diagonals.
"""

import numpy as np

def find_main_diagonal_color(grid):
    # Find the color of the main diagonal (top-left to bottom-right).
    for i in range(min(grid.shape)):
        if grid[i, i] != 0:
            return grid[i, i]
    return 0  # Should not usually happen in the given context.

def find_secondary_diagonal(grid, diagonal_color):
    # Find secondary diagonal.
    n,m = grid.shape
    new_grid = np.copy(grid)
    for i in range(n):
        for j in range(m):
          if i + j == n -1 and new_grid[i,j] == 0:
             new_grid[i,j] = diagonal_color

    return new_grid
            

def remove_block(grid, diagonal_color):
    # Set cells not on diagonals and not equal to background (0) to 0.
    n,m = grid.shape
    new_grid = np.copy(grid)
    for i in range(n):
        for j in range(m):
            if (i!=j and i+j != n-1)  and new_grid[i,j]!=0:
                new_grid[i, j] = 0
    return new_grid

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)

    # Find color of the main diagonal
    diagonal_color = find_main_diagonal_color(output_grid)
   
    # Remove any non-diagonal elements.
    output_grid = remove_block(output_grid, diagonal_color)

    # Draw secondary diagonal
    output_grid = find_secondary_diagonal(output_grid,diagonal_color)
    

    return output_grid.tolist()
```
