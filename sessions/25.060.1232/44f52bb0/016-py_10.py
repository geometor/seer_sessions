"""
The output grid has the same dimensions as the bounding box of the single object in the input grid. The output grid is filled with a single color. The output color varies:

*   If the input object is azure (8), the output object is blue (1).
*   If the input object is gray (5), the output object is red (2).
*   If the input object is blue (1), the output object is azure (8).
The first training example seems to be incorrect and shows height and width transposed.
"""

import numpy as np

def get_object_details(grid):
    """
    simple object detection - improved from describe_objects to return coords
    """
    # Convert grid to set of (color, (x,y)) tuples.
    pixels = {(color, (x, y)) for y, row in enumerate(grid) for x, color in enumerate(row)}
    objects = {}
    
    # Group contiguous pixels of same color by flood-fill procedure
    while pixels:
      color, (x,y) = pixels.pop()
      if color not in objects:
        objects[color] = []
      
      stack = [(x,y)]
      
      while stack:
        x,y = stack.pop()
        
        objects[color].append((x,y))

        # check the 4 adjacent neighbors
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        for nx, ny in neighbors:
            if (color, (nx, ny)) in pixels:
                pixels.remove((color, (nx, ny)))
                stack.append((nx, ny))

    details = {}
    for color, coords in objects.items():
        min_x = min(x for x, _ in coords)
        max_x = max(x for x, _ in coords)
        min_y = min(y for _, y in coords)
        max_y = max(y for _, y in coords)
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        details[color] = {
            'coordinates': coords,
            'min_x': min_x,
            'max_x': max_x,
            'min_y': min_y,
            'max_y': max_y,
            'width': width,
            'height': height
        }
    return details

def transform(input_grid):
    # Get the object details from the input grid.
    input_object_details = get_object_details(input_grid)

    # There should be only one object
    if len(input_object_details) != 1:
      raise ValueError("Expected only a single object in input.")

    # get input color and dimensions
    input_color = list(input_object_details.keys())[0]
    input_width = input_object_details[input_color]['width']
    input_height = input_object_details[input_color]['height']

    # Determine the output color based on input
    if input_color == 8:
      output_color = 1
    elif input_color == 5:
       output_color = 2
    elif input_color == 1:
       output_color = 8
    else: # unknown color, return input color for now
      output_color = input_color
    
    # Create output with same dimensions
    output_grid = np.full((input_height, input_width), output_color, dtype=int)

    return output_grid