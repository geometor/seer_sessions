"""
1.  **Extract Pattern:** Identify the 3x3 subgrid at the top-left corner of the input grid as the repeating pattern.

2.  **Replicate Pattern:** Tile this 3x3 pattern across the output grid. The output grid cell at `(i, j)` gets its initial value from the input grid cell at `(i % 3, j % 3)`.

3.  **Fill White Pixels (Zero Values):** For every white pixel (value 0) in the output grid, replace its value with the nearest non-white pixel within the same 3x3 cell. The "same 3x3 cell" is defined by the replication process. Specifically, if a pixel is at (i, j) in the output grid, we consider the non zero pixels in its neighborhood.
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