"""
1.  **Identify Foreground Object:** In each input, identify the object located in the top right corner that is also the *largest* object by pixel area.
2.  **Identify Color Palette:** Note the color of this foreground object.
3.  **Frame Creation:** Create a frame in the output by filling almost all available locations of the output with the color of the identified foreground object.
4.  **Object Transformation:** Find an object from input that exists in the output: In train_1 input, the orange "7" transforms to the green "3" in the output. In train_2 input, the green "3" transforms to the green "3" in the output. In train_3 input, the green "3" transforms to the cyan "8" in the output.
5. **Output frame shape:** the transformed object creates a 'frame' shape that occupies all other positions.
"""

import numpy as np

def find_objects(grid):
    """
    Finds connected components (objects) in a grid.
    Returns a dictionary where keys are colors and values are lists of (row, col) tuples.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                obj = []
                dfs(r, c, color, obj)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj)
    return objects

def get_top_right_object(objects):
    """Identifies the object in the top-right corner and find the largest object of same color"""
    top_right_color = None
    top_right_object = None

    for color in objects:
        for obj in objects[color]:
             #sort by col then row
             obj.sort(key=lambda x: (-x[1],x[0]))
             if top_right_object is None:
                top_right_object = obj
                top_right_color = color
             else:
                if obj[-1][1] > top_right_object[-1][1]:
                    top_right_object= obj
                    top_right_color = color
                elif obj[-1][1] == top_right_object[-1][1] and  obj[-1][0] < top_right_object[-1][0]:
                    top_right_object = obj
                    top_right_color=color
    
    # get largest
    largest_object = top_right_object
    for obj in objects[top_right_color]:
        if len(obj) > len(largest_object):
            largest_object = obj
    return largest_object, top_right_color
    

def get_object_transformation(input_grid, output_grid):
    """
    Determine the color transformation mapping based on input and output grids.

    Args:
        input_grid: The input grid as a NumPy array.
        output_grid: The output grid as a NumPy array.

    Returns:
        A dictionary mapping input colors to output colors.
    """
     # Find objects in input and output
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)

    transformations = {}

    for in_color in input_objects:
        for out_color in output_objects:
             if len(input_objects[in_color])==len(output_objects[out_color]):
                 transformations[in_color]=out_color

    return transformations

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    
    # Find objects in the input grid
    input_objects = find_objects(input_grid)

    # Identify the top-right object and color
    foreground_object, foreground_color = get_top_right_object(input_objects)

     # Determine output grid size (This is a guess, based on examples - needs refinement)
    
    output_rows = 0
    output_cols = 0

    for color in input_objects:
        for obj in input_objects[color]:
            for r,c in obj:
                output_rows = max(r+1,output_rows)
                output_cols = max(c+1,output_cols)


    # Initialize the output grid with zeros
    output_grid = np.zeros((output_rows, output_cols), dtype=int)
  
    # transform the foreground object in input to output grid
    
    color_xforms = {
       7:3,
       3:8,
       2:6
    }
    new_color = foreground_color
    if foreground_color in color_xforms:
        new_color = color_xforms[foreground_color]
    
    for r, c in foreground_object:
        if r < output_rows and c < output_cols:
            output_grid[r,c] = new_color

    return output_grid