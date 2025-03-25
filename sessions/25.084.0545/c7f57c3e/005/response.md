```python
"""
The transformation rule identifies objects in both input and output grids, maps them based on color, size, shape, and proximity, and then performs actions like move, transform (color/size/shape change), create, or delete to generate the output. The background color is preserved. Objects are sorted by size before mapping, largest first.
"""

import numpy as np
from collections import Counter

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
                    bounds = calculate_object_bounds(region)
                    objects.append({
                        "id": obj_id_counter,
                        "color": color,
                        "pixels": region,
                        "shape": get_object_shape(region),
                        "size": len(region),
                        "min_row": bounds[0][0],
                        "min_col": bounds[0][1],
                        "max_row": bounds[1][0],
                        "max_col": bounds[1][1],
                    })
                    obj_id_counter += 1
    return objects

def get_background_color(grid):
    """Determines the background color."""
    return Counter(grid.flatten()).most_common(1)[0][0]

def calculate_distance(bounds1, bounds2):
    """Calculates the distance between the centers of two bounding boxes."""
    center1_r = (bounds1[0][0] + bounds1[1][0]) / 2
    center1_c = (bounds1[0][1] + bounds1[1][1]) / 2
    center2_r = (bounds2[0][0] + bounds2[1][0]) / 2
    center2_c = (bounds2[0][1] + bounds2[1][1]) / 2
    return np.sqrt((center1_r - center2_r)**2 + (center1_c - center2_c)**2)

def transform_object(output_grid, input_obj, output_obj):
    """Transforms an input object to match the output object."""
    # Clear the old pixels of the input object, respecting background
    background_color = get_background_color(output_grid)
    for r, c in input_obj['pixels']:
        output_grid[r, c] = background_color
    
    # Calculate transformation parameters
    dr = output_obj['min_row'] - input_obj['min_row']
    dc = output_obj['min_col'] - input_obj['min_col']

    # Apply transformation: move and change color/size if necessary
    new_pixels = []
    for r, c in input_obj['pixels']:
        new_r = r + dr
        new_c = c + dc
        if 0 <= new_r < output_grid.shape[0] and 0 <= new_c < output_grid.shape[1]:
            output_grid[new_r, new_c] = output_obj['color']
            new_pixels.append((new_r, new_c))

    
    remaining_pixels = output_obj['size'] - len(new_pixels)
    if remaining_pixels > 0:
      # Create new pixels if output object is bigger
       
      r,c = new_pixels[-1] # start at the last placed pixel
      
      
      for _ in range(remaining_pixels):
        neighbors = [(r+1,c), (r-1, c), (r,c+1), (r, c-1)]
        valid_neighbors = []
        for nr, nc in neighbors:
           if 0<= nr < output_grid.shape[0] and 0<= nc < output_grid.shape[1]:
              valid_neighbors.append((nr,nc))
        
        if len(valid_neighbors) > 0:

            r,c = valid_neighbors[0]
            output_grid[r,c] = output_obj['color']
            new_pixels.append((r,c))

    elif remaining_pixels < 0:
       # remove pixels if output obj is smaller
        new_pixels = new_pixels[:output_obj['size']]
        for r,c in new_pixels:
           output_grid[r,c] = output_obj['color']

    
    input_obj['pixels'] = new_pixels
    input_obj['color'] = output_obj['color'] # update to new color
    input_obj['min_row'] = output_obj['min_row']
    input_obj['min_col'] = output_obj['min_col']
    input_obj['shape'] = get_object_shape(new_pixels)
    input_obj['size'] = len(new_pixels)

    return output_grid
   

def create_object(output_grid, output_obj):

   new_obj = {
        'id': -1, # Placeholder ID, will be corrected later
        'color': output_obj['color'],
        'pixels': [],
        'shape':output_obj['shape'],
        'size': output_obj['size'],
        'min_row': output_obj['min_row'],
        'min_col': output_obj['min_col']
    }
   
   r = output_obj['min_row']
   c = output_obj['min_col']

   for i in range(output_obj['size']):
      if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
            output_grid[r, c] = output_obj['color']
            new_obj['pixels'].append((r, c))
      if output_obj['shape'] == 'line':
         if output_obj['max_row'] > output_obj['min_row']:
            r+=1
         else:
            c+=1
      else:
         c+=1 # make lines, and rectangles
         if i > 0 and (i+1) % (output_obj['max_col'] - output_obj['min_col']+1) == 0 :
            r+=1
            c = output_obj['min_col']

   new_obj['size'] = len(new_obj['pixels']) # update the object size

   return output_grid, new_obj


def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    background_color = get_background_color(input_grid)

    # Find objects in the input and output grids
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)

    # Sort objects by size (descending)
    input_objects.sort(key=lambda obj: obj["size"], reverse=True)
    output_objects.sort(key=lambda obj: obj["size"], reverse=True)
    
    
    # Map output objects to input objects
    matched_input_objects = []
    created_objects = []

    for output_obj in output_objects:
        best_match = None
        best_score = float('inf')

        for input_obj in input_objects:
            if input_obj in matched_input_objects:
                continue  # Skip already matched input objects

            # Calculate matching score
            score = 0

            # 1. Color match
            if input_obj['color'] == output_obj['color']:
                score -= 1  # Prefer color match (negative score for better match)

            # 2. Size difference
            score += abs(input_obj['size'] - output_obj['size'])

            # 3. Shape
            if input_obj['shape'] == output_obj['shape']:
               score -=1

            # 4. Distance between objects
            input_bounds = calculate_object_bounds(input_obj['pixels'])
            output_bounds = calculate_object_bounds(output_obj['pixels'])
            score += calculate_distance(input_bounds, output_bounds)

            if score < best_score:
                best_score = score
                best_match = input_obj

        if best_match is not None:
            # Transform the best matching object
            output_grid = transform_object(output_grid, best_match, output_obj)
            matched_input_objects.append(best_match)

        else:
            # Create a new object
           
            output_grid, new_obj = create_object(output_grid, output_obj)
            if len(new_obj['pixels'])> 0:
              created_objects.append(new_obj)
    
    # Correct the IDs of created objects
    next_id = max([obj['id'] for obj in input_objects], default=-1) + 1
    for obj in created_objects:
      obj['id'] = next_id
      next_id+=1

    return output_grid
```