```python
"""
Iterate through white pixels. For each white pixel, check its 4-connected neighbors. If a neighbor is blue, change the blue neighbor to orange, unless doing so would create a 2x2 orange block or the white pixel is part of an enclosed group of white pixels.
"""

import numpy as np

def get_neighbors(grid, row, col, connectivity=4):
    """
    Get the neighbors of a pixel in the grid.
    connectivity: 4 or 8 (default 4)
    """
    rows, cols = grid.shape
    neighbors = []
    if connectivity == 4:
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    else:  # connectivity == 8
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    for dr, dc in deltas:
        neighbor_row, neighbor_col = row + dr, col + dc
        if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
            neighbors.append((neighbor_row, neighbor_col))
    return neighbors

def is_2x2_orange(grid, row, col):
    """
    Checks if changing the pixel at (row, col) to orange would create a 2x2 orange block.
    """
    rows, cols = grid.shape
    if not (0 <= row < rows and 0 <= col < cols):
        return False

    for r in range(max(0, row - 1), min(rows, row + 2)):
        for c in range(max(0, col - 1), min(cols, col + 2)):
            if (r + 1 < rows and c + 1 < cols):
                if (grid[r, c] == 7 and grid[r + 1, c] == 7 and
                    grid[r, c + 1] == 7 and grid[r + 1, c + 1] == 7):
                    return True
    return False
    

def is_enclosed(grid, row, col):
    """
    Checks if the white pixel at (row, col) is part of an enclosed group of white pixels.
    """
    rows, cols = grid.shape
    visited = set()
    stack = [(row, col)]

    while stack:
        curr_row, curr_col = stack.pop()
        if (curr_row, curr_col) in visited:
            continue
        visited.add((curr_row, curr_col))

        if curr_row == 0 or curr_row == rows - 1 or curr_col == 0 or curr_col == cols - 1:
            return False  # Reached an edge

        for neighbor_row, neighbor_col in get_neighbors(grid, curr_row, curr_col, 4):
            if grid[neighbor_row, neighbor_col] == 0:
                stack.append((neighbor_row, neighbor_col))

    return True  # No path to edge found


def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check if it's a white pixel
            if output_grid[row, col] == 0:
                # check that white region is not enclosed
                if is_enclosed(output_grid,row,col):
                    continue

                # Get neighbors
                neighbors = get_neighbors(output_grid, row, col, 4)
                
                # check neighbors
                for n_row, n_col in neighbors:
                    # change blue neighbor to orange
                    if output_grid[n_row,n_col] == 1:
                         # check if change would make 2x2
                        if not is_2x2_orange(output_grid,n_row,n_col):
                            output_grid[n_row,n_col] = 7

    return output_grid
```