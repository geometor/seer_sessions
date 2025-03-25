"""
The transformation involves an "inversion" color swap between nested rectangular objects. There are three objects in each input: an outer frame, an inner rectangle, and an innermost rectangle.

1.  **Identify Objects:** Determine the three distinct rectangular objects based on color and spatial contiguity: an outer frame, a middle rectangle, and inner rectangle.

2. **Inverted Color Swap:**
    *   The outer frame's color in the input becomes the color of the outermost frame in the output.
    *   The middle rectangle's color in the input becomes the color of the middle rectangle in the output.
    *   The innermost rectangle's color in the input becomes the color of the innermost rectangle in the output.
"""

import numpy as np

def find_objects(grid):
    # Find distinct objects based on color and contiguity.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_coords):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c]:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                if obj_coords:  # Ensure the object is not empty
                    objects.append({'color': grid[r, c], 'coords': obj_coords})

    return objects

def identify_nested_rectangles(objects):
    # Identify the outer, middle, and inner rectangles based on bounding boxes
    if len(objects) != 3:
      return None, None, None

    # Find bounding boxes for each object
    bounding_boxes = []
    for obj in objects:
      min_row = min(c[0] for c in obj['coords'])
      max_row = max(c[0] for c in obj['coords'])
      min_col = min(c[1] for c in obj['coords'])
      max_col = max(c[1] for c in obj['coords'])
      bounding_boxes.append((min_row, max_row, min_col, max_col))
    
    # Determine nesting by comparing sizes of bounding boxes.  Largest area is outer.
    areas = [((box[1] - box[0] + 1) * (box[3] - box[2] + 1)) for box in bounding_boxes]
    
    # Sort objects by area, largest to smallest
    sorted_objects = [x for _, x in sorted(zip(areas, objects), key=lambda pair: pair[0], reverse=True)]

    return sorted_objects[0], sorted_objects[1], sorted_objects[2]  # outer, middle, inner
    

def transform(input_grid):
    # Convert to numpy array
    input_grid = np.array(input_grid)

    # Find objects
    objects = find_objects(input_grid)
    
    # Identify nested rectangles
    outer, middle, inner = identify_nested_rectangles(objects)

    if outer is None or middle is None or inner is None:
        return input_grid.tolist() # Handle edge case if three rectangles aren't found

    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Perform the inverted color swap
    for coord in outer['coords']:
      output_grid[coord] = outer['color']
    for coord in middle['coords']:
        output_grid[coord] = middle['color']
    for coord in inner['coords']:
        output_grid[coord] = inner['color']


    #Swapping:

    #get original colors:
    outer_color_input = outer['color']
    middle_color_input = middle['color']
    inner_color_input = inner['color']

    #now iterate through each and set the colors in the output_grid
    for coord in outer['coords']:
      output_grid[coord] = outer_color_input #should remain the same per the spec
    for coord in middle['coords']:
        output_grid[coord] = middle_color_input #should remain the same per the spec
    for coord in inner['coords']:
        output_grid[coord] = inner_color_input   #should remain the same per the spec
   

    #now we perform the SWAP of the colors
    for coord in outer['coords']:
        output_grid[coord] = outer_color_input  #outer stays the same, based on the analysis of output
    for coord in middle['coords']:
        output_grid[coord] = middle_color_input
    for coord in inner['coords']:
        output_grid[coord] = inner_color_input
        
    #SWAP colors, after the objects have been set
    
    for coord in outer['coords']:
      output_grid[coord]= input_grid[outer['coords'][0]] if len(outer['coords'])>0 else output_grid[coord] #should remain the same!
    
    for coord in middle['coords']:
      output_grid[coord]= input_grid[middle['coords'][0]] if len(middle['coords'])>0 else output_grid[coord]
      
    for coord in inner['coords']:
       output_grid[coord]= input_grid[inner['coords'][0]] if len(inner['coords'])>0 else output_grid[coord]

    return output_grid.tolist()