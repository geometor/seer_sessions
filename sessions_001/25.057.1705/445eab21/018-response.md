# 445eab21 • 018 • refine_coder

---
```python
"""
Transforms the input grid based on the location and size of a blue object.
If the blue object is a single pixel, the output is a 1x1 grid with that pixel.
If the blue object is larger, the output is a 2x2 grid containing the blue object.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects of the same color in a grid.
    Returns a dictionary where keys are colors and values are lists of pixel coordinates.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj_pixels):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj_pixels.append((r, c))
        dfs(r + 1, c, color, obj_pixels)
        dfs(r - 1, c, color, obj_pixels)
        dfs(r, c + 1, color, obj_pixels)
        dfs(r, c - 1, color, obj_pixels)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                if color != 0:  # Ignore background
                    obj_pixels = []
                    dfs(r, c, color, obj_pixels)
                    if color not in objects:
                        objects[color] = []
                    objects[color].append(obj_pixels)
    return objects

def get_bounding_box(pixels):
    """
    Returns the bounding box (min_row, min_col, max_row, max_col) of a list of pixels.
    """
    rows, cols = zip(*pixels)
    return min(rows), min(cols), max(rows), max(cols)

def transform(input_grid):
    """
    Transforms the input grid based on the location of the blue object.
    """
    objects = find_objects(input_grid)
    
    # Locate Blue Object
    if 1 in objects:  # Blue is color 1
        blue_objects = objects[1]
        
        # ARC tasks typically involve only one object of a given non-background color
        if len(blue_objects) > 0:
           blue_object = blue_objects[0] # use the first blue object

           # Determine output grid size
           if len(blue_object) == 1:
               # single pixel object
               r, c = blue_object[0]
               output_grid = np.array([[input_grid[r,c]]])
           else:
               # find a 2x2 area that contains part of the blue object.
               min_r, min_c, max_r, max_c = get_bounding_box(blue_object)
               
               # find best 2x2 area containing some blue
               best_r, best_c = -1,-1
               for r in range(min_r,max_r):
                  for c in range(min_c,max_c):
                     if r+1 <= max_r and c+1 <= max_c:
                        if input_grid[r:r+2,c:c+2].shape == (2,2):
                            # found a valid 2x2
                            if best_r == -1:
                               best_r = r
                               best_c = c
                            
                            num_blue = 0
                            for br in range(r,r+2):
                               for bc in range(c,c+2):
                                  if (br,bc) in blue_object:
                                      num_blue+=1

                            best_num_blue = 0
                            for br in range(best_r,best_r+2):
                               for bc in range(best_c, best_c+2):
                                 if (br,bc) in blue_object:
                                     best_num_blue +=1
                            if num_blue > best_num_blue:
                                 # use area with the most blue
                                 best_r = r
                                 best_c = c
                                 
               if best_r != -1:
                   output_grid = input_grid[best_r:best_r+2, best_c:best_c+2]
               else:
                   # fall back - use a corner
                   output_grid = input_grid[min_r:min_r+2, min_c:min_c+2]

        else: # no blue objects
             output_grid = np.zeros_like(input_grid) # return all zeros
    else:  # No blue object found
        output_grid = np.zeros_like(input_grid)  # Or some other default behavior

    return output_grid
```

