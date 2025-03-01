"""
1.  **Identify Azure Objects:** Locate all contiguous blocks of azure (color 8) pixels in the input grid.
2.  **Prioritize Top-Right Object**: If there are multiple azure objects and any has pixels where x > 5, consider *only* the object at the top-right of the input grid.
3.  **Apply the shift, if any:** If the remaining object consists of single pixels (i.e many small objects), shift each azure pixel down by one row and combine them to adjacent pixels on that row.
4.  **Apply Horizontal Translation:** If the selected object has a width greater than it's height, translate the entire object to the right edge, then shift left 3 units.
"""

import numpy as np

def find_objects(grid, color):
    coords = np.argwhere(grid == color)
    if len(coords) == 0:
        return []  # Return empty list if no objects of specified color
    # Group contiguous pixels into objects
    objects = []
    visited = set()
    for x, y in coords:
        if (x, y) not in visited:
            object_coords = []
            stack = [(x, y)]
            while stack:
                curr_x, curr_y = stack.pop()
                if (curr_x, curr_y) in visited:
                    continue
                visited.add((curr_x, curr_y))
                object_coords.append((curr_x, curr_y))
                # Check adjacent pixels (up, down, left, right)
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_x, new_y = curr_x + dx, curr_y + dy
                    if (0 <= new_x < grid.shape[0] and 0 <= new_y < grid.shape[1] and
                            grid[new_x, new_y] == color and (new_x, new_y) not in visited):
                        stack.append((new_x, new_y))
            objects.append(object_coords)
    return objects

def get_object_extents(obj):
    """returns xmin, xmax, ymin, ymax"""
    xmin = min(x for x, y in obj)
    xmax = max(x for x, y in obj)
    ymin = min(y for x, y in obj)
    ymax = max(y for x, y in obj)
    return xmin, xmax, ymin, ymax

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find all azure objects
    azure_objects = find_objects(input_grid, 8)

    # Prioritize Top-Right object, if it exists
    if len(azure_objects) > 1:
        top_right_object = None
        for obj in azure_objects:
            xmin, xmax, ymin, ymax = get_object_extents(obj)
            if xmax > 5: # Check for pixels in the top-right area
                if top_right_object == None:
                     top_right_object = obj
                else:
                    #pick the object farthest to the right
                    tr_xmin, tr_xmax, tr_ymin, tr_ymax = get_object_extents(top_right_object)
                    if xmax > tr_xmax:
                        top_right_object = obj

        if top_right_object != None:
            #clear all objects
            for obj in azure_objects:
                 for x, y in obj:
                    output_grid[x, y] = 0  # Clear
            azure_objects = [top_right_object] #keep only this object
            for x, y in top_right_object:
                output_grid[x,y] = 8



    if len(azure_objects) == 1: #we have only one azure object
        obj = azure_objects[0]
        xmin, xmax, ymin, ymax = get_object_extents(obj)
        width = xmax - xmin + 1
        height = ymax - ymin + 1
        #clear the object
        for x, y in obj:
             output_grid[x,y] = 0

        if width > height:  # Rule for horizontal translation
            #translate to right edge, then three units to the left
            new_ymin = input_grid.shape[1] - width -3 #right edge
            for x, y in obj:
                output_grid[x, new_ymin + (y - ymin )] = 8
        else: #single pixels
             #shift down one row
            for x, y in obj:
                new_x = x+1
                if new_x < output_grid.shape[0]:
                    #find nearest open spot to the right
                    for i in range(output_grid.shape[1]):
                        if output_grid[new_x, min(y+i, output_grid.shape[1]-1)] == 0:
                            output_grid[new_x, min(y+i, output_grid.shape[1]-1)] = 8
                            break
                        elif output_grid[new_x, max(y-i, 0)] == 0:
                            output_grid[new_x, max(y-i, 0)] = 8
                            break
    elif len(azure_objects) > 1 : #we have only single pixels
        #clear all objects
        for obj in azure_objects:
            for x, y in obj:
                output_grid[x, y] = 0  # Clear

        for obj in azure_objects: #should only be single points here
            for x, y in obj:
                new_x = x+1
                if new_x < output_grid.shape[0]:
                    #find nearest open spot to the right
                    for i in range(output_grid.shape[1]):
                        if output_grid[new_x, min(y+i, output_grid.shape[1]-1)] == 0:
                            output_grid[new_x, min(y+i, output_grid.shape[1]-1)] = 8
                            break
                        elif output_grid[new_x, max(y-i, 0)] == 0:
                            output_grid[new_x, max(y-i, 0)] = 8
                            break


    return output_grid