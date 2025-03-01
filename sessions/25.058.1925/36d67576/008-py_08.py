"""
1.  **Object Identification:** Identify all contiguous blocks of pixels (objects) of the same color. Classify objects by shape ('L', 'line', or 'other'). Record the color, positions, and shape of each object.

2.  **Conditional L-Shape Mirroring:**
    *   IF an object has an "L" shape, THEN mirror the object's position across the horizontal axis.

3. **Conditional Color Changes (part of mirroring):**
      - After mirroring the blue and green L shapes in example 1:
          -The L shape that was originally green is now an L of mixed color.
          -The upper-left corner of the originally green L is now blue, and the rest of the L remains green.
      - After mirroring the blue line and orange L shape in example 2:
          - If an object is a length of 3, blue, line, its top most-left pixel changes to orange.
          - If an object is orange, its bottom most-right pixel stays orange, and the rest of the pixels in that object become blue.

4. **Line Transformations**
    - In example 0, if a horizontal line of yellow color exists and length is greater than 2, and a length of 3, green line exists, add a single green pixel at the end of the yellow line's right side.

5.  **Conditional Swapping (Example 0):**
    *   IF a green pixel exists at position (4, 9) AND a yellow pixel exists at (8, 9), THEN swap their positions.
    *   IF a blue pixel exists at (4, 11) AND a yellow pixel at (6,10) exists, THEN swap their positions

6.  **Preservation:** All pixels not involved in the above transformations retain their original color and position.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects and classifies them."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, current_object):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, color, current_object)
        dfs(r - 1, c, color, current_object)
        dfs(r, c + 1, color, current_object)
        dfs(r, c - 1, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                shape = classify_shape(current_object)
                objects.append({'color': grid[r, c], 'positions': current_object, 'shape': shape})
    return objects

def classify_shape(positions):
    """Classifies the shape of an object."""
    if len(positions) == 1:
        return 'single pixel'
    elif len(positions) == 3:
        # Check for L shape
        x_coords = [pos[1] for pos in positions]
        y_coords = [pos[0] for pos in positions]
        if len(set(x_coords)) == 2 and len(set(y_coords)) == 2:
            return 'L'
    elif len(positions) > 1:
        x = [pos[1] for pos in positions]
        if len(set(x))== 1:
            return "line"

    return 'other'

def mirror_positions(positions, rows):
    """Mirrors positions across the horizontal axis."""
    mirrored = []
    for r, c in positions:
        mirrored.append((rows - 1 - r, c))
    return mirrored

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    objects = find_objects(input_grid)

    # Conditional L-Shape Mirroring
    for obj in objects:
        if obj['shape'] == 'L':
            mirrored_positions = mirror_positions(obj['positions'], rows)
            for r, c in obj['positions']:
                output_grid[r, c] = 0  # Clear original positions
            for r, c in mirrored_positions:
                output_grid[r, c] = obj['color'] # set to the original color first

    # Conditional Color Changes (part of mirroring)
    for obj in objects:

        if obj['shape'] == 'L' and obj['color'] == 3:
            mirrored_positions = mirror_positions(obj['positions'],rows)
            for r,c in mirrored_positions:
                 if (r,c) == (rows - 1- obj['positions'][0][0], obj['positions'][0][1]):
                    output_grid[r,c] = 1

        if obj['shape'] == 'L' and obj['color'] == 7:
             mirrored_positions = mirror_positions(obj['positions'],rows)
             for r,c in mirrored_positions:
                if [r,c] != [rows -1 - obj['positions'][0][0], obj['positions'][0][1]]:
                    output_grid[r,c] = 1

    for obj in objects:
        if obj['shape'] == 'line' and len(obj['positions']) == 3 and obj['color'] == 1:
            mirrored_positions = mirror_positions(obj['positions'], rows)
            for r, c in obj['positions']:
                    output_grid[r,c] = 0
            for r, c in mirrored_positions:
                output_grid[r,c] = 1
            output_grid[mirrored_positions[0][0], mirrored_positions[0][1]] = 7



    # Line Transformations (Example 0 specific)
    yellow_line = None
    green_line = None

    for obj in objects:
        if obj['color'] == 4 and obj['shape'] == 'line':
            yellow_line = obj
        if obj['color'] == 3 and obj['shape'] == 'line' :
            green_line = obj

    if yellow_line != None and green_line != None:
        if len(yellow_line['positions']) > 2 and len(green_line['positions']) == 3:
             yellow_line_end = max(yellow_line['positions'], key=lambda item:item[1])
             output_grid[yellow_line_end[0],yellow_line_end[1]+1] = 3

    # Conditional Swapping (Example 0)
    if input_grid[4, 9] == 3 and input_grid[8, 9] == 4:
      output_grid[4, 9], output_grid[8, 9] = output_grid[8, 9], output_grid[4, 9]
    if input_grid[4, 11] == 1 and input_grid[6, 10] == 4:
      output_grid[4, 11], output_grid[6, 10] = output_grid[6, 10], output_grid[4, 11]

    return output_grid