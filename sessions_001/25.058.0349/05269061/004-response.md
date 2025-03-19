# 05269061 • 004 • refine_coder

---
```python
"""
1.  **Pattern Extraction:** Extract the 3x3 subgrid from the top-left corner of the input grid. This is the repeating pattern.

2.  **Pattern Replication:** Replicate this 3x3 pattern across the entire output grid, tiling it both horizontally and vertically.  This means the output grid's values at `(i, j)` will initially be set to the input grid's values at `(i % 3, j % 3)`.

3.  **Zero Filling (Corrected):** After the pattern replication, iterate through the output grid. For each cell containing a 0 (white), find the nearest, non-zero pixel, treating the grid as a connected space of individual 3x3 cells (from step 2).
    - Use the value of that non-zero neighbor to fill.

In other words, propagate the color from non-zero "seed" pixels to all connected zero-value neighbors using the repeating 3 x 3 cell as a guide for propagation.
"""

import numpy as np

def get_neighbors(i, j, height, width):
    """
    Get valid neighbors of a cell (i,j) in a grid.
    """
    neighbors = []
    if i > 0:
        neighbors.append((i-1,j))
    if i < height - 1:
        neighbors.append((i+1,j))
    if j > 0:
        neighbors.append((i,j-1))
    if j < width -1:
        neighbors.append((i, j+1))

    return neighbors
    

def propagate_color(output_grid, i, j, height, width, visited):
    """
    Propagate color to connected regions using a stack, handling the 3x3 cell boundaries.

    Args:
        grid (np.array): The input/output grid.
        i (int): starting row index.
        j (int): starting col index.
        height, width: dimensions of the grid
        visited: set of visited cells.

    """

    stack = [(i,j)]
    while stack:
        curr_i, curr_j = stack.pop()

        if (curr_i, curr_j) in visited:
            continue
        visited.add((curr_i,curr_j))

        # Determine the base 3x3 cell indices
        base_i = curr_i % 3
        base_j = curr_j % 3
        
        # find non-zero color source in this cell
        non_zero_color = None
        for ni,nj in get_neighbors(base_i,base_j, 3, 3):
            seed_i, seed_j = curr_i + (ni-base_i),curr_j+(nj-base_j)
            # boundary check
            if 0 <= seed_i < height and 0 <= seed_j < width:
                if output_grid[seed_i, seed_j] != 0:
                    non_zero_color = output_grid[seed_i, seed_j]
                    break # found a source
        if non_zero_color is None: # no source found, look in seed cell
             if output_grid[curr_i - base_i, curr_j - base_j] !=0:
                non_zero_color = output_grid[curr_i-base_i, curr_j-base_j]


        if non_zero_color is not None:
            output_grid[curr_i, curr_j] = non_zero_color

            for ni, nj in get_neighbors(curr_i, curr_j, height, width):
                if output_grid[ni,nj] == 0:
                    stack.append((ni,nj))


def transform(input_grid):
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros((height, width), dtype=int)

    # 1. & 2. Pattern Replication
    for i in range(height):
        for j in range(width):
            output_grid[i, j] = input_grid[i % 3, j % 3]

    # 3. Zero Filling (Corrected)
    visited = set()
    for i in range(height):
        for j in range(width):
            if output_grid[i,j] == 0 and (i,j) not in visited:
                propagate_color(output_grid,i,j,height, width, visited)


    return output_grid.tolist()
```
