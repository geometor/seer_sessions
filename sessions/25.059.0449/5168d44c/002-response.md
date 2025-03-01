# 5168d44c • 002 • example_3 • investigate_coder

---
```python
"""
The transformation identifies connected components of red (2) pixels and isolated or contained green (3) pixels.
It then shifts or copies the connected red block upwards while keeping green (3) pixels within it intact.
It also maintains the vertical order of green pixels, and empties the red block's original position.
"""

import numpy as np
from scipy.ndimage import label, find_objects

def find_connected_components(grid, color):
    """Finds connected components of a specific color in the grid."""
    colored_grid = (grid == color).astype(int)
    labeled_grid, num_features = label(colored_grid)
    return labeled_grid, num_features

def get_object_slices(labeled_grid, num_features):
    """Gets the slices for each connected component."""
    return find_objects(labeled_grid)

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    
    # Find connected components of red (2)
    red_labeled_grid, red_num_features = find_connected_components(input_grid, 2)
    red_slices = get_object_slices(red_labeled_grid, red_num_features)

    # Find green pixels and their locations
    green_pixels = np.argwhere(input_grid == 3)
    
    # Iterate through red components and move/copy
    if red_num_features > 0:
        for red_slice in red_slices:
           
            red_block = input_grid[red_slice]
            
            # compute output location 
            row_shift = red_block.shape[0]
            
            output_row_start = red_slice[0].start - row_shift
            output_row_end = red_slice[0].stop - row_shift

            if output_row_start >= 0:
               output_grid[output_row_start:output_row_end, red_slice[1]] = red_block
               
            # empty the original position of red pixels
            red_rows = np.where((input_grid == 2).any(axis=1))[0]

            for r in red_rows:
                 if all(val == 0 or val == 2 or val == 3 for val in input_grid[r,:]):
                    output_grid[r,:] = 0
            
            # move green color inside the red block
            for green_pixel in green_pixels:
              if red_slice[0].start <= green_pixel[0] < red_slice[0].stop and red_slice[1].start <= green_pixel[1] < red_slice[1].stop:
                  output_grid[green_pixel[0] - row_shift, green_pixel[1] ] = 3
                  output_grid[green_pixel[0], green_pixel[1]] = 0


    # Handle green pixels outside of red blocks (maintain relative vertical order)
    green_pixels = np.argwhere(input_grid == 3)
    
    shifted_green_pixels = []

    for i in range(len(green_pixels)):
        
        found = False

        for red_slice in red_slices:
           
            red_block = input_grid[red_slice]
            
            row_shift = red_block.shape[0]

            if red_slice[0].start <= green_pixels[i][0] < red_slice[0].stop and red_slice[1].start <= green_pixels[i][1] < red_slice[1].stop:
                 shifted_green_pixels.append([green_pixels[i][0] - row_shift, green_pixels[i][1]])
                 found = True
                 break;
        
        if not found:
            shifted_green_pixels.append([green_pixels[i][0], green_pixels[i][1]])
    
    # sort by original positions
    sorted_green = sorted(zip(green_pixels, shifted_green_pixels), key = lambda x: (x[0][0],x[0][1]))
    
    #remove the original green positions
    for green_pixel in green_pixels:
        is_red = False
        for red_slice in red_slices:
           if red_slice[0].start <= green_pixel[0] < red_slice[0].stop and red_slice[1].start <= green_pixel[1] < red_slice[1].stop:
                is_red = True
                break

        if not is_red: output_grid[green_pixel[0], green_pixel[1]] = 0

    #fill by new green positions
    for (original, shifted) in sorted_green:
          if shifted[0] >= 0:  # Ensure we don't go out of bounds
            output_grid[shifted[0], shifted[1]] = 3

    return output_grid
```
