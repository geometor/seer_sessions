# 3906de3d • 008 • refine_coder

---
```python
"""
1.  **Identify the Blue Anchor:** Find the blue (color 1) object. This is considered the "anchor".
2. **Identify all other objects:** Find all contiguous blocks of pixels of the same color (other than color 0 - background), and record their positions *relative* to the blue anchor (above or below).
3. **Determine movement of blue:** determine if the blue object has shifted vertically
4. **Stack other objects:**
    * Objects should maintain their relative vertical order with respect to each other.
    * Objects that were initially *below* the blue anchor should be stacked *directly* below the blue anchor, with the closest object adjacent to the anchor.
    * If the blue object has moved up: Objects that were initially *above* the blue anchor are moved down to fill the space *directly* above it, maintaining their relative order and adjacency to blue.
5.  **Background:** The background (color 0) remains unchanged.
"""

import numpy as np
from scipy.ndimage import measurements

def find_objects(grid):
    # use scipy.ndimage.measurements.label to find contiguous regions
    labeled_grid, num_objects = measurements.label(grid)
    objects = []
    for i in range(1, num_objects + 1):  # Iterate through labeled objects (excluding background)
        coords = np.argwhere(labeled_grid == i)
        if coords.size == 0: #handle edge case
            continue
        color = grid[coords[0][0], coords[0][1]] #color of object
        min_row, min_col = np.min(coords, axis=0)
        max_row, max_col = np.max(coords, axis=0)
        width = max_col - min_col + 1
        height = max_row - min_row + 1
        objects.append({
            'color': color,
            'coords': coords,
            'top_row': min_row,
            'bottom_row': max_row,
            'left_col': min_col,
            'right_col': max_col,
            'width': width,
            'height': height
        })
    return objects

def find_blue_anchor(objects):
    # find blue anchor within list of objects
    for obj in objects:
        if obj['color'] == 1:
            return obj
    return None

def get_relative_position(obj, blue_anchor):
    # determine position of an object relative to the blue anchor
    if blue_anchor is None: #handle edge case
      return "no_blue" #no anchor
    if obj['bottom_row'] < blue_anchor['top_row']:
        return 'above'
    elif obj['top_row'] > blue_anchor['bottom_row']:
        return 'below'
    else:
        return 'overlap' #shouldn't happen in this task

def move_object(grid, coords, delta_row, delta_col):
    #generic move
    new_coords = coords + np.array([delta_row, delta_col])
    color = grid[coords[0][0], coords[0][1]]

    # erase from old
    for r, c in coords:
        grid[r, c] = 0

    # place in new 
    for r, c in new_coords:
        grid[r, c] = color
    return grid

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find all objects
    objects = find_objects(input_grid)

    # Find the blue anchor object.
    blue_anchor = find_blue_anchor(objects)
    if blue_anchor is None: #return input if no blue
        return output_grid

    # Separate objects based on their relative position to the blue anchor.
    above_objects = []
    below_objects = []
    for obj in objects:
        if obj['color'] != 1:  # Exclude the blue anchor itself
            relative_pos = get_relative_position(obj, blue_anchor)
            if relative_pos == 'above':
                above_objects.append(obj)
            elif relative_pos == 'below':
                below_objects.append(obj)

    # Sort objects by their top row to maintain relative order.
    above_objects = sorted(above_objects, key=lambda x: x['top_row'], reverse=True)
    below_objects = sorted(below_objects, key=lambda x: x['top_row'])


    # determine blue anchor movement
    output_blue_anchor = find_blue_anchor(find_objects(output_grid)) #find blue anchor position in the output
    blue_delta_row = output_blue_anchor['top_row'] - blue_anchor['top_row']


    # move blue anchor
    if blue_delta_row !=0:
        output_grid = move_object(output_grid, blue_anchor['coords'], blue_delta_row,0)
        blue_anchor = find_blue_anchor(find_objects(output_grid)) #update after move


    # stack below objects below the blue anchor
    current_row = blue_anchor['bottom_row'] + 1
    for obj in below_objects:
        delta_row = current_row - obj['top_row']
        output_grid = move_object(output_grid, obj['coords'], delta_row, 0)
        current_row += obj['height']  # Increment current_row by object height

    # stack above objects, if blue has moved up
    if blue_delta_row > 0:
      current_row = blue_anchor['top_row'] -1
      for obj in above_objects:
        delta_row = current_row - obj['bottom_row']
        output_grid = move_object(output_grid, obj['coords'], delta_row,0)
        current_row -= obj['height']

    return output_grid
```
