```python
import numpy as np
from collections import Counter, defaultdict

"""
Transformation Rule:

1. Determine the background color by finding the most frequent pixel color in the input grid.
2. Identify all distinct objects (contiguous blocks of the same non-background color) in the input grid.
3. For each object, determine its bounding box, shape (relative pixel coordinates), and whether its bounding box contains any background pixels not part of the object itself ('contains_background').
4. Count the frequency of each unique object shape in the input grid.
5. Select objects to keep if they either 'contain_background' or their shape appears more than once (frequency > 1).
6. Identify the single kept object that 'contains_background'; its color becomes the 'fill_color' for the output grid.
7. Calculate the minimal bounding box enclosing all kept objects.
8. Create the output grid with the dimensions of the minimal bounding box, initialized with the 'fill_color'.
9. Draw the kept objects onto the output grid at their relative positions within the minimal bounding box, overwriting the 'fill_color'.
"""

def find_objects(grid, background_color):
    """
    Finds all connected objects of non-background colors in the grid.
    Uses Breadth-First Search (BFS).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != background_color:
                color = grid[r, c]
                obj_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.pop(0)
                    obj_pixels.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                objects.append({
                    'color': color,
                    'pixels': frozenset(obj_pixels), # Use frozenset for hashability
                    'bounding_box': (min_r, min_c, max_r, max_c)
                })
    return objects

def get_relative_shape(pixels, min_r, min_c):
    """
    Calculates the shape of an object relative to its top-left corner.
    Returns a hashable representation (sorted tuple of relative coordinates).
    """
    relative_pixels = sorted([(r - min_r, c - min_c) for r, c in pixels])
    return tuple(relative_pixels)

def check_contains_background(grid, obj, background_color):
    """
    Checks if the object's bounding box contains background pixels
    that are not part of the object itself.
    """
    min_r, min_c, max_r, max_c = obj['bounding_box']
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if (r, c) not in obj['pixels'] and grid[r, c] == background_color:
                return True
    return False

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # 1. Determine background color
    background_color = Counter(input_grid.flatten()).most_common(1)[0][0]

    # 2. Identify all objects
    objects = find_objects(input_grid, background_color)

    if not objects:
        # Handle case with no non-background objects (though unlikely in ARC)
        return np.array([[background_color]]) 

    # 3. & 4. Calculate properties (shape, contains_background) and shape frequency
    shape_counts = defaultdict(int)
    for obj in objects:
        min_r, min_c, _, _ = obj['bounding_box']
        obj['shape'] = get_relative_shape(obj['pixels'], min_r, min_c)
        obj['contains_background'] = check_contains_background(input_grid, obj, background_color)
        shape_counts[obj['shape']] += 1

    for obj in objects:
        obj['shape_frequency'] = shape_counts[obj['shape']]

    # 5. Select kept objects
    kept_objects = []
    for obj in objects:
        if obj['contains_background'] or obj['shape_frequency'] > 1:
            kept_objects.append(obj)

    if not kept_objects:
         # Handle case where no objects are kept (unlikely based on examples)
         # Returning a minimal grid with background might be a fallback,
         # but let's follow the logic assuming kept objects exist per examples.
         # Based on example 1, if only one object qualifies, it's the fill object.
         # Let's assume at least one object is kept.
         # If this assumption fails on test cases, we might need to adjust.
         print("Warning: No objects were kept.")
         # Defaulting to a 1x1 grid of background might be safest if truly empty.
         return np.array([[background_color]])


    # 6. Find fill object and color
    fill_object = None
    for obj in kept_objects:
        if obj['contains_background']:
            if fill_object is not None:
                # Error: More than one object contains background
                # This contradicts the assumption based on examples.
                # Let's proceed with the first one found for now.
                print("Warning: Multiple objects contain background. Using the first one found.")
            fill_object = obj
            #break # Assuming only one such object based on examples.
    
    if fill_object is None:
        # Error: No kept object contains background.
        # This also contradicts the assumption. What should the fill be?
        # Maybe default to the general background? Or the color of the first kept object?
        # Let's default to the input background color as a fallback.
        print("Warning: No kept object contains background. Using input background as fill.")
        fill_color = background_color
    else:
        fill_color = fill_object['color']


    # 7. Calculate minimal bounding box for kept objects
    if not kept_objects: # Should not happen if previous checks are robust, but defensive coding
         return np.array([[fill_color]]) # Return 1x1 grid with fill color

    min_r_out = min(obj['bounding_box'][0] for obj in kept_objects)
    min_c_out = min(obj['bounding_box'][1] for obj in kept_objects)
    max_r_out = max(obj['bounding_box'][2] for obj in kept_objects)
    max_c_out = max(obj['bounding_box'][3] for obj in kept_objects)

    out_height = max_r_out - min_r_out + 1
    out_width = max_c_out - min_c_out + 1

    # 8. Create output grid initialized with fill_color
    output_grid = np.full((out_height, out_width), fill_color, dtype=input_grid.dtype)

    # 9. Place kept objects onto the output grid
    for obj in kept_objects:
        obj_color = obj['color']
        for r, c in obj['pixels']:
            out_r = r - min_r_out
            out_c = c - min_c_out
            # Check bounds just in case, though theoretically unnecessary if BB is correct
            if 0 <= out_r < out_height and 0 <= out_c < out_width:
                 output_grid[out_r, out_c] = obj_color

    return output_grid.tolist() # Return as list of lists per ARC standard
```