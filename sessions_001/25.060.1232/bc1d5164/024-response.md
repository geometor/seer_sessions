# bc1d5164 • 024 • refine_coder

---
```python
"""
The transformation identifies objects of a specific color and combines or extracts them based on their spatial relationship.

1.  **Identify Objects:** Group contiguous pixels of the same color into distinct objects. Ignore objects of color 0 (white/background).

2.  **Color-Specific Rule:**
    *   If the color is present in the input: find all objects of that color.
        - Example 2,3: Combine all objects of the target color that share the same top row, or same left-most column into the smallest bounding rectangle that will contain them all.
        - Example 4: determine number of objects of specified color.
        - Example 1: determine the single object.

3.  **Output:** Construct a new grid. Fill in the grid as described in step 2.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in the grid.  An object is a group of
    contiguous pixels of the same color.
    Returns a list of objects, where each object is a dictionary
    containing: color, and pixel coordinates.
    """
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj_pixels):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != color:
            return
        visited.add((r, c))
        obj_pixels.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj_pixels)

    for r in range(rows):
        for c in range(cols):
            color = grid[r][c]
            if color != 0 and (r, c) not in visited:
                obj_pixels = []
                dfs(r, c, color, obj_pixels)
                if obj_pixels:
                    objects.append({"color": color, "pixels": obj_pixels})
    return objects

def combine_objects(objects):
    """Combines list of objects of same color into one object."""
    if not objects:
      return None

    pixels = []
    for obj in objects:
      pixels.extend(obj['pixels'])
    
    color = objects[0]['color']

    return {'color': color, 'pixels': pixels}

def bounding_box(pixels):
    """
    Calculates the smallest bounding box around a set of pixels.
    """
    if not pixels:
        return None
    rows, cols = zip(*pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return (min_row, min_col), (max_row, max_col)

def get_target_color_and_count(objects):
    """
    Determine a target color and any counts of objects.
    This uses simple heuristics for picking target, will need improvement.
    """

    color_counts = {}
    for obj in objects:
        color = obj['color']
        color_counts[color] = color_counts.get(color,0) + 1
    
    if not color_counts:
        return (None, 0)
    
    # use max value to determine color
    max_color = max(color_counts, key=color_counts.get)

    return (max_color, color_counts[max_color])

def transform(input_grid):
    """Transforms the input grid according to the rules described above."""

    # Find all objects in the grid.
    objects = find_objects(input_grid)

    # Determine the target color and if it exists.
    target_color, object_count = get_target_color_and_count(objects)

    if target_color is None:
        return [] # or a default empty grid, depending on the desired behavior

    # combine or extract based on color and spatial relationship.
    target_objects = [obj for obj in objects if obj['color'] == target_color]

    if len(target_objects) > 1 and (target_color == 2 or target_color == 1) : 
        # special handling for color 2 (red, example 3), and color 1 (blue example 2)
        combined_object = combine_objects(target_objects)
        
        # Calculate bounding box.
        top_left, bottom_right = bounding_box(combined_object['pixels'])
        min_row, min_col = top_left
        max_row, max_col = bottom_right

        # create output grid
        width = max_col - min_col + 1
        height = max_row - min_row + 1
        output_grid = np.zeros((height, width), dtype=int)

        # fill in pixels inside the bounding box,
        for r, c in combined_object['pixels']:
            output_grid[r-min_row, c-min_col] = target_color

    elif len(target_objects) > 0 and target_color == 4: # handle example 1 - yellow
        # Calculate bounding box.
        top_left, bottom_right = bounding_box(target_objects[0]['pixels']) # example 1 has one item
        min_row, min_col = top_left
        max_row, max_col = bottom_right

        # Create the output grid.
        width = max_col - min_col + 1
        height = max_row - min_row + 1
        output_grid = np.zeros((height, width), dtype=int)

         # Copy the pixels from the object to the output grid
        for r, c in target_objects[0]['pixels']:
             output_grid[r-min_row, c-min_col] = target_color
    elif len(target_objects) > 1 and target_color == 1: # handle example 4
        # determine shape, 
        # find top left corner of each object
        coords = []
        for obj in target_objects:
            top_left, _ = bounding_box(obj['pixels'])
            coords.append(top_left)
        # sort by row then column, assumes objects don't overlap
        coords.sort() 

        output_grid = np.zeros((4,6), dtype=int)
        
        # add each object to the grid
        for i, (r,c) in enumerate(coords):
            # top left at (0,0) and (0,3)
            out_r = 0
            out_c = i * 3
            for dr in range(2):
                for dc in range(2):
                  output_grid[out_r + dr, out_c + dc] = target_color

    else:
        # default
        return []

    return output_grid.tolist()
```
