"""
1. Identify Objects: Determine all contiguous regions of the same color within the input grid. These are the objects.
2. Left Section Copy: Copy the leftmost four columns (columns 0-3) of the input grid directly to the output grid without any changes.
3. Rightmost Object in Left Section: Among the objects identified, find the one that extends furthest to the right within the copied left section (columns 0-3).
4. Transformation based on Objects:
    * If there is a special case where there are 2 objects of the same color, and the color ==1, then a mirroring of the left section is performed: the left section is flipped across both axes, and then flipped horizontally, then combined.
    *  Else, the rightmost object found in step 3 is repeated in the right section.
5. Object Repetition:
    Repeat the object identified from the previous step. Determine repetition count and spacing dynamically.
6.  Output: The resulting grid is the final output.
"""

import numpy as np

def find_objects(grid):
    """Finds distinct objects in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, object_coords):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        object_coords.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, object_coords)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                object_coords = []
                dfs(r, c, grid[r, c], object_coords)
                if object_coords:
                    objects.append({
                        'color': grid[r, c],
                        'coords': object_coords
                    })
    return objects

def get_rightmost_object(objects):
    """Identifies the right-most object within the first four columns."""
    rightmost_object = None
    max_col = -1

    for obj in objects:
        for r, c in obj['coords']:
            if c <= 3:  # Consider only objects within the first four columns
                if c > max_col:
                    max_col = c
                    rightmost_object = obj
    return rightmost_object

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Copy the left section (first four columns)
    output_grid[:, :4] = input_grid[:, :4]

    # Find objects
    objects = find_objects(input_grid)

    # Find rightmost object in the left section
    rightmost_object = get_rightmost_object(objects)

    # Transformation based on Objects: Special case handling
    if len(objects) == 2 and objects[0]['color'] == objects[1]['color'] and objects[0]['color'] == 1:
        left_section = input_grid[:, :4]
        # Mirrored across both axes
        mirrored_section = np.flip(left_section, axis=(0, 1))
        output_grid[:, 4:7] = mirrored_section[:, 1:]

        # Inverted (flipped horizontally)
        inverted_section = np.flip(left_section, axis=1)
        output_grid[:, 7:11] = inverted_section

    # General case: Object Repetition (if not the special mirroring case)
    elif rightmost_object:
        # Determine object dimensions
        obj_width = max(c for _, c in rightmost_object['coords']) - min(c for _, c in rightmost_object['coords']) + 1
        
        # Calculate Dynamic Spacing
        obj_coords = sorted(rightmost_object['coords'], key=lambda item: item[1])
        if len(obj_coords)>1:
            spacing = obj_coords[1][1] - obj_coords[0][1] 
        else: 
            spacing = 1

        # Repeat the object.
        start_col = 4  # Start placing repetitions after the copied section

        # Calculate Repetitions (dynamic)
        reps = (cols - start_col) // (obj_width + spacing -1 )
        reps = min(reps,2) # cap repetitions

        for i in range(reps):
            for r, c in rightmost_object['coords']:
                new_r = r
                new_c = start_col + (c - min(cc for _, cc in rightmost_object['coords'])) + i * (obj_width + spacing - 1)

                if new_c < cols:
                    output_grid[new_r, new_c] = rightmost_object['color']

    return output_grid