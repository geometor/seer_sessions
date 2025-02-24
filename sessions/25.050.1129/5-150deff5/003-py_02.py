"""
The transformation rule is as follows:
1. Identify the Object: Find the contiguous region of color '5' (gray) in the input grid. This is our primary object.
2. Substitution 1: Every other cell of color 5 will be substituted by the color 8. Starting from coordinate [1,1].
3. Substitution 2: Every cell with value 0 and inside the object 1 (that is, surrounded by color 5 objects) will turn into color 2.
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of all cells with the specified color.
    coords = np.argwhere(grid == color)
    return coords

def is_inside(grid, coord, object_coords):
    x, y = coord
    
    if any(np.array_equal(coord,obj_coord) for obj_coord in object_coords):
       return False
        
    #check west
    west = False
    for i in range(0,x):
        if [i,y] in object_coords.tolist():
          west = True

    east = False
    for i in range(x,grid.shape[0]):
        if [i,y] in object_coords.tolist():
          east = True
          
    north = False
    for i in range(0,y):
        if [x,i] in object_coords.tolist():
          north = True

    south = False
    for i in range(y,grid.shape[1]):
        if [x,i] in object_coords.tolist():
          south = True
          
    return west and east and north and south

def transform(input_grid):
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)

    # Find the object with color 5.
    object_coords = find_object(input_grid, 5)

    # Change color 5 to color 8.
    count = 0
    for coord in object_coords:
        if count % 2 == 0:
          output_grid[coord[0], coord[1]] = 8
        count+=1

    # Find cells with color 0 inside the object and change them to 2.
    for x in range(output_grid.shape[0]):
        for y in range(output_grid.shape[1]):
            if output_grid[x, y] == 0:
              if is_inside(input_grid, [x,y], object_coords):
                output_grid[x, y] = 2

    return output_grid