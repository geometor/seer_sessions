# a1570a43 • 012 • refine_coder

---
```python
"""
1.  **Identify Objects:**
    *   Find the contiguous "red block" (color 2).
    *   Find all "green pixels" (color 3).

2.  **Transformation Rule:**
    *   If the green pixels form a surrounding frame and there is a single green pixel in the direct center of the red block, and the red block forms a horizontal line, the red block rotates 90 degrees clockwise around that center green pixel.
    *  If the green pixels form a surrounding frame and the red block forms a horizontal line segment and its center aligns with a green center, rotate the segment.
    *   If the green pixels form a surrounding frame and the red block is a vertical line, the red block translates horizontally such that its leftmost pixel aligns with the column where the original rightmost red pixel was present.
    *   All green pixels remain in their original positions.

3. **Output:** create a new grid with the red block after the transformation and preserve original green pixels
"""

import numpy as np

def get_red_block(grid):
    # Find coordinates of all red pixels
    return np.argwhere(grid == 2)

def get_green_pixels(grid):
    # Find coordinates of all green pixels
    return np.argwhere(grid == 3)

def is_horizontal(coords):
  #check that all coordinates are on the same row
  return all([coords[0][0] == c[0] for c in coords])

def is_vertical(coords):
    #check that all coordinates are on the same column
    return all([coords[0][1] == c[1] for c in coords])

def rotate_90(coords, center):
    # Rotate coordinates 90 degrees clockwise around a center point
    centered_coords = coords - center
    rotated_coords = np.array([[-y, x] for x, y in centered_coords])
    return rotated_coords + center

def transform(input_grid):
    # Initialize output grid with the green pixels in the same positions
    output_grid = np.copy(input_grid)
    output_grid[output_grid == 2] = 0 # remove original red

    # Get the red block and green pixels coordinates
    red_block = get_red_block(input_grid)
    green_pixels = get_green_pixels(input_grid)

    # 1. Horizontal line, single center green pixel
    if is_horizontal(red_block) and len(red_block) > 1:
      
        #find center of the red block
        min_x = min(red_block[:,0])
        max_x = max(red_block[:,0])
        min_y = min(red_block[:,1])
        max_y = max(red_block[:,1])

        center = np.array([(min_x + max_x)/2 , (min_y + max_y)/2])
        
        rotated_red_block = rotate_90(red_block, center)
        rotated_red_block = np.round(rotated_red_block).astype(int) #convert back

        #place back into array
        for x, y in rotated_red_block:
           if 0 <= x < output_grid.shape[0] and 0 <= y < output_grid.shape[1]:
               output_grid[x,y] = 2

    #3 vertical line translate horizontally
    elif is_vertical(red_block) and len(red_block) > 1:
        #get rightmost pixel coordinate column
        rightmost_col = max(red_block[:,1])
        #shift each x
        
        translated_red_block = []
        for x,y in red_block:
            new_y = rightmost_col
            translated_red_block.append( (x,new_y) )

        for x, y in translated_red_block:
          if 0 <= x < output_grid.shape[0] and 0 <= y < output_grid.shape[1]:
              output_grid[x,y]=2
    
    #else don't move anything
    else:
        for x, y in red_block:
            output_grid[x,y] = 2


    return output_grid
```
