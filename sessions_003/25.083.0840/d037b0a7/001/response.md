```python
"""
1.  **Identify non-zero color values that is not touching a zero.** Starting from the top-left of the grid.
2.  **Propagate, non-zero color to fill zeros along the bottom row, then the bottom-right direction.** If the original color is to the left of non-zero, continue to fill bottom until complete. If the original color is on the right, continue to fill the bottom-right diagonal.
3.  **Stop propagation** when encountering a non-zero value, a zero, or the edge of the grid.
"""

import numpy as np

def get_neighbors(grid, r, c):
    """get all neighbors, diagonals included, skip out of bounds"""

    rows, cols = grid.shape
    neighbors = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue

            rr, cc = r + i, c + j
            if 0 <= rr < rows and 0 <= cc < cols:
                neighbors.append(grid[rr,cc])
    
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    #iterate thru grid
    for r in range(rows):
        for c in range(cols):
            #find any nonzeros
            if input_grid[r,c] != 0:
                neighbors = get_neighbors(input_grid,r,c)

                #check if any neighbors are zero
                if 0 not in neighbors:
                    color = input_grid[r,c]

                    #fill bottom
                    for i in range(r + 1, rows):
                        if output_grid[i,c] == 0:
                            output_grid[i,c] = color
                        else:
                            break

                    # fill bottom-right diagonal
                    rr, cc = r + 1, c+1
                    while rr < rows and cc < cols:
                        if output_grid[rr,cc] == 0:
                             output_grid[rr,cc] = color
                        else:
                            break
                        
                        rr += 1
                        cc += 1


    return output_grid
```