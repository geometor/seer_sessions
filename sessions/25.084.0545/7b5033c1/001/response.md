```python
"""
The input grid is scanned from top to bottom. Contiguous vertical runs of non-8 (non-white) colors are identified.  The unique colors from these runs are extracted and output in a 1D list, maintaining the order in which they appear in the input grid.
"""

import numpy as np

def get_object_widths(input_grid):
    """
    Helper function to get the start, end and color of each object.
    """
    objects = []
    
    for x in range(0,input_grid.shape[1]):
      in_obj = False
      cur_obj = -1
      obj_start = -1
      
      for y in range(0, input_grid.shape[0]):
        pix = input_grid[y,x]
        
        if pix != 8 and in_obj == False:
          in_obj = True
          cur_obj = pix
          obj_start = x
        elif pix != cur_obj and in_obj == True:
          objects.append( (obj_start, x-1, cur_obj))
          if pix != 8:
             in_obj = True
             cur_obj = pix
             obj_start = x
          else:
            in_obj = False
            cur_obj = -1
            obj_start = -1

      if in_obj:
        objects.append( (obj_start, x, cur_obj) )

    return objects

def transform(input_grid):
    """
    Transforms a 2D input grid into a 1D output list based on the described rule.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # get object widths and colors
    objects = get_object_widths(input_grid)

    # Initialize an empty output list
    output_list = []

    # Iterate through the identified objects
    for start, end, color in objects:
      for i in range(start, end + 1):
        output_list.append(color)

    return output_list
```