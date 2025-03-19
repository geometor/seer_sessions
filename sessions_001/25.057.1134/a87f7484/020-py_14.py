"""
The transformation rule extracts the smallest square subgrid from the top-left corner of the input grid that contains all non-zero pixels connected to the top-left corner pixel.
"""

import numpy as np

def find_connected_component(grid, start_row, start_col):
    """
    Finds the connected component of non-zero pixels starting from a given cell using Depth-First Search (DFS).
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    component = []

    def dfs(row, col):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] == 0
        ):
            return
        visited[row, col] = True
        component.append((row, col))
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    dfs(start_row, start_col)
    return component

def transform(input_grid):
    """
    Extracts the smallest square subgrid from the top-left corner of the input grid
    that contains all non-zero pixels connected to the top-left corner pixel.
    """
    input_grid = np.array(input_grid)
    
    # Find the connected component starting from the top-left corner (0, 0)
    if input_grid[0,0] == 0:
      first_object = [(0,0)]
    else:
      first_object = find_connected_component(input_grid, 0, 0)

    # Determine the boundaries of the connected component
    if not first_object:
        max_row, max_col = 0, 0
    else:
      max_row = max(cell[0] for cell in first_object)
      max_col = max(cell[1] for cell in first_object)
    
    #Determine the size
    size = max(max_row, max_col) + 1

    # Extract the subgrid.
    output_grid = input_grid[0:size, 0:size]

    return output_grid.tolist()