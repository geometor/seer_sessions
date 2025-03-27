"""
The transformation rule identifies contiguous regions of the same color as distinct objects. It detects changes by comparing the input and output grids.
For each changed pixel location in the output, it finds a matching object in the input grid, or creates a new object if no exact match is found.
The best match is moved to the target location. Objects can be moved or created. Objects left behind are deleted.
The most frequent color in the grid is considered the background and remains unchanged.
"""

import numpy as np
from collections import Counter

def find_objects(grid):
    """Identifies contiguous regions of the same color as distinct objects."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, color, obj_id):
        if (r < 0 or r >= rows or c < 0 or c >= cols or visited[r, c] or grid[r, c] != color):
            return []
        visited[r, c] = True
        region = [(r, c)]
        region.extend(dfs(r + 1, c, color, obj_id))
        region.extend(dfs(r - 1, c, color, obj_id))
        region.extend(dfs(r, c + 1, color, obj_id))
        region.extend(dfs(r, c - 1, color, obj_id))
        return region

    obj_id_counter = 0
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                color = grid[r, c]
                region = dfs(r, c, color, obj_id_counter)
                if region:
                    objects.append({
                        "id": obj_id_counter,
                        "color": color,
                        "pixels": region,
                        "shape": "irregular",  # Initial shape
                        "size": len(region)
                    })
                    obj_id_counter +=1
    return objects

def calculate_object_bounds(pixels):
    """Calculate the bounding box of an object."""
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    for r, c in pixels:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return (min_r, min_c), (max_r, max_c)

def get_object_shape(pixels):
   bounds = calculate_object_bounds(pixels)
   height = bounds[1][0] - bounds[0][0] + 1
   width = bounds[1][1] - bounds[0][1] + 1

   if height == 1 or width == 1:
      return "line"
   if height == width:
       return "square"
   return "rectangle"




def find_best_match(input_objects, color, size, shape, target_r, target_c, output_grid):
    """Find the best matching object in the input grid."""
    best_match = None
    best_score = -1

    for obj in input_objects:
           
        # Check if the object can explain the changed pixel
        
        # Calculate object dimensions
        bounds = calculate_object_bounds(obj['pixels'])
        obj_height = bounds[1][0] - bounds[0][0] + 1
        obj_width = bounds[1][1] - bounds[0][1] + 1
        
        
        if obj['color'] == color and len(obj['pixels']) >=1: #size
            score = 0
            
            if get_object_shape(obj['pixels']) == shape:
               score +=1
           
            
            # Prioritize objects with some overlap with existing
            overlap = False
            for r,c in obj['pixels']:
               if 0 <= target_r < output_grid.shape[0] and 0<= target_c < output_grid.shape[1]:

                   if output_grid[r,c] == obj['color']:
                      overlap = True
                      break
            if overlap:
               score+=2
            
            if score > best_score:
               best_score = score
               best_match = obj


    return best_match

def move_object(grid, obj, target_r, target_c):
    """Moves an object to a new location."""
    new_grid = np.copy(grid)
    # Calculate object bounds
    bounds = calculate_object_bounds(obj['pixels'])
    obj_height = bounds[1][0] - bounds[0][0] + 1
    obj_width = bounds[1][1] - bounds[0][1] + 1

    # Calculate the offset
    dr = target_r - bounds[0][0]
    dc = target_c - bounds[0][1]

     #Clear old position, but preserve background
    for r,c in obj['pixels']:
        new_grid[r,c] = get_background_color(grid)
    
    # Move object
    new_pixels = []
    for r, c in obj['pixels']:
         new_r = r + dr
         new_c = c + dc
         if 0<= new_r < new_grid.shape[0] and 0 <= new_c < new_grid.shape[1]:
            new_grid[new_r, new_c] = obj['color']
            new_pixels.append((new_r, new_c))
    obj['pixels'] = new_pixels #update object pixels

    return new_grid, obj

def get_background_color(grid):
    """Determines the background color."""
    return Counter(grid.flatten()).most_common(1)[0][0]

def create_object(color, size, shape, r, c, output_grid):
    new_obj = {
        'id': -1, # Placeholder ID, will be corrected later
        'color': color,
        'pixels': [],
        'shape':shape,
        'size': size
    }

    height = 0
    width = 0
    if shape == 'square':
       height = int(np.sqrt(size))
       width = int(np.sqrt(size))
    elif shape == 'rectangle':

        if r+1 < output_grid.shape[0] and output_grid[r,c] != output_grid[r+1,c]:
            width = size
            height = 1
        elif c+1 < output_grid.shape[1] and output_grid[r,c] != output_grid[r,c+1]:
            height = size
            width = 1
    elif shape == 'line':
         if r+1 < output_grid.shape[0] and output_grid[r,c] == output_grid[r+1,c]:
             height = size
             width=1
         elif c+1 < output_grid.shape[1] and output_grid[r,c] == output_grid[r,c+1]:
             width = size
             height = 1
    
    for i in range(height):
        for j in range(width):
             curr_r = r + i
             curr_c = c + j
             if 0<= curr_r < output_grid.shape[0] and 0<= curr_c < output_grid.shape[1]:
                new_obj['pixels'].append((curr_r,curr_c))
                output_grid[curr_r,curr_c] = color

    return output_grid, new_obj

def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    background_color = get_background_color(input_grid)

    # Find objects in the input grid
    input_objects = find_objects(input_grid)
    created_objects = []

    # Detect changed pixels (between input and expected output, in practice we don't have this)
    # Here, for demonstration purposes, I assume a hypothetical 'expected_output'
    # In a real scenario, we would analyze changes and infer them.
    
    # Find changes
    changed_pixels = []
    for obj in find_objects(output_grid):
        initial_color = -1
        for r,c in obj['pixels']:
           if input_grid[r,c] != output_grid[r,c]:
              initial_color = input_grid[r,c]
              changed_pixels.append((r,c,obj['color'], initial_color, get_object_shape(obj['pixels']), obj['size']))

    
    processed = []
    for r, c, new_color, initial_color, shape, size in changed_pixels:
        
      if (r,c) not in processed:
        # Find the best matching object
        best_match = find_best_match(input_objects, new_color,size, shape, r,c, output_grid) # use output grid for overlap detection

        if best_match is not None:
            # Move the object
            output_grid, best_match = move_object(output_grid, best_match, r, c)
            for rp, cp in best_match['pixels']:
                processed.append((rp,cp))
        else:

            output_grid, new_obj = create_object(new_color, size, shape, r, c, output_grid)
            if len(new_obj['pixels']) > 0:
               created_objects.append(new_obj)
            for rp, cp in new_obj['pixels']:
                processed.append((rp,cp))
    
    # Correct the IDs of created objects
    next_id = max([obj['id'] for obj in input_objects], default=-1) + 1
    for obj in created_objects:
      obj['id'] = next_id
      next_id+=1


    return output_grid