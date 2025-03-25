"""
Create green (3) vertical bars of height 2 under two horizontally adjacent pixels of different colors. If there are two-colored object, the space between them that is only one row, it gets filled with two green vertical bars with height 2.
"""

import numpy as np

def find_objects(grid):
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                obj = []
                if c + 1 < cols and grid[r,c] != grid[r,c+1] and grid[r,c+1] !=0:
                    
                    obj.append((r,c))
                    obj.append((r,c+1))
                    visited[r,c]=True
                    visited[r,c+1]=True
                    objects.append(obj)

    return objects


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    objects = find_objects(input_grid)
    
    for obj in objects:
      for cell in obj:
        r,c = cell
        if r + 1 < rows:
           output_grid[r+1,c] = 3
        if r + 2 < rows:
           output_grid[r+2,c] = 3
    
    #Fill spaces between objects:
    for r in range(rows-2):
      for obj1 in objects:
        for obj2 in objects:
            if obj1[0][0] == r and obj2[0][0] == r + 2: #check for two row apart objects.
                if obj1[0][1] == obj2[0][1]:
                  for cell in obj1:
                    output_grid[r+1, cell[1]]=3

    return output_grid