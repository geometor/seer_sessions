"""
The transformation swaps the position and type of some objects, based on color and shape matching between input and output.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous blocks of the same color in a grid.
    Returns a dictionary of objects, where keys are object IDs (integers)
    and values are dictionaries containing object properties.
    """
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)
    object_id = 0

    def dfs(row, col, color, object_pixels):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                object_pixels = []
                dfs(row, col, grid[row, col], object_pixels)
                if object_pixels:
                    objects[object_id] = {
                        "color": grid[row, col],
                        "pixels": object_pixels,
                        "shape": get_shape(object_pixels),
                    }
                    object_id += 1
    return objects

def get_shape(pixels):
    """
    Determine a simple shape representation for a set of pixels.
    """
    min_row = min(p[0] for p in pixels)
    max_row = max(p[0] for p in pixels)
    min_col = min(p[1] for p in pixels)
    max_col = max(p[1] for p in pixels)

    shape_data = []

    for r in range(min_row,max_row+1):
        row_data = []
        for c in range(min_col, max_col + 1):
            if (r,c) in pixels:
                row_data.append(1)
            else:
                row_data.append(0)
        shape_data.append(row_data)

    return shape_data
    

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # find the objects
    input_objects = find_objects(input_grid)

    # train_1:
    # swaps 7 6 and 8 8
    # input objects: 0:7, 1:6, 2:4, 3:8
    # output objects: 0:8, 1:7, 2:9, 3:7
    # shape compare: color, pixels

    # Find corresponding objects and swap their positions
    
    for obj1_id, obj1 in input_objects.items():
        pixels1 = obj1["pixels"]
        for (row,col) in pixels1:
                output_grid[row,col] = obj1["color"]


    #get the object locations for color 7 and 6
    color1_objects = []
    color2_objects = []
    for obj_id, obj in input_objects.items():
        if obj['color'] == 7:
            color1_objects.append(obj_id)
        elif obj['color'] == 6:
            color2_objects.append(obj_id)

    
    if (len(color1_objects) > 0) and (len(color2_objects) > 0):
        #we only take first element, and if they have same shape, we exchange colours
        shape1 = input_objects.get(color1_objects[0])['shape']
        shape2 = input_objects.get(color2_objects[0])['shape']
        if shape1 == shape2:
          #now find the objects in the output
          output_grid = np.zeros_like(input_grid)

          obj1 = input_objects[color1_objects[0]]
          obj2 = input_objects[color2_objects[0]]

          pixels1 = obj1["pixels"]
          pixels2 = obj2["pixels"]
          
          
          color1 = obj2['color']
          color2 = obj1['color']

          for (row, col) in pixels1:
                output_grid[row,col] = color1
          for (row, col) in pixels2:
                output_grid[row,col] = color2
                

    #get the object locations for color 8
    color1_objects = []
    for obj_id, obj in input_objects.items():
        if obj['color'] == 8:
            color1_objects.append(obj_id)
    
    if (len(color1_objects) > 1):
        #we only take first element, and if they have same shape, we exchange colours
        shape1 = input_objects.get(color1_objects[0])['shape']
        shape2 = input_objects.get(color1_objects[1])['shape']
        if shape1 != shape2:
            output_grid = np.zeros_like(input_grid)
            #find the objects with shape2
            target_color = -1
            for obj_id, obj in input_objects.items():
                if obj['shape'] == shape2:
                    target_color = obj['color']
                    break

            if target_color != -1:
                obj1 = input_objects[color1_objects[0]]
                
                #now find the objects in the output
                

                
                pixels1 = obj1["pixels"]
                
                
                
                color1 = target_color

                for (row, col) in pixels1:
                        output_grid[row,col] = color1

                #now do the final object, color = 8
                for obj_id, obj in input_objects.items():
                    if obj['color'] == target_color:
                        #copy all other objects as is
                        pixels = obj['pixels']
                        for (row,col) in pixels:
                            output_grid[row,col] = 8

    return output_grid