```python
"""
1.  **Locate Gray Pixels:** Identify all gray pixels (value 5) in the *input* grid. These are the "seed" locations.

2.  **Create 3x3 Blue Blocks, Centered:** For *each* gray pixel found in the input grid, create a 3x3 block of blue pixels (value 1) in the *output* grid. The gray pixel's original location should be the *center* of this 3x3 blue block.

3.  **Conditional Expansion based on Input:** Iterate through all the cells of *output*. Expand the blue color (1) outwards from each of the created 3x3 blocks *only* to the directly adjacent pixels (up, down, left, right, and diagonals) if the corresponding cell in the *input* grid is white (value 0). Do *not* expand from the newly created blue pixels, only from the original 3x3 blue blocks placed in step 2.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Get the 8 neighbors of a pixel (Moore neighborhood).
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append((i, j))
    return neighbors

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Locate Gray Pixels and 2. Create 3x3 Blue Blocks
    gray_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5:
                gray_pixels.append((r, c))
                for i in range(max(0, r - 1), min(rows, r + 2)):
                    for j in range(max(0, c - 1), min(cols, c + 2)):
                        output_grid[i, j] = 1

    # 3. Conditional Expansion based on Input
    for r, c in gray_pixels:
        for nr, nc in get_neighbors(input_grid, r, c): #check neighbors of the *original* grey
            if input_grid[nr, nc] == 0: # check if original input was white
                 for i in range(max(0, r - 1), min(rows, r + 2)): # iterate *original* 3x3
                    for j in range(max(0, c - 1), min(cols, c + 2)):
                        for nnr, nnc in get_neighbors(output_grid, i, j):
                            if input_grid[nnr,nnc] == 0:
                                output_grid[nnr,nnc] = 1

    return output_grid.tolist()
```