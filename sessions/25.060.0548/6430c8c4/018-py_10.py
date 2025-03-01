"""
1.  **Identify the Target Object:** Find the contiguous block of pixels that are *not* color 0 (white/background) that is closest to the top-left corner of the input grid. "Closest" means the object whose top-left corner pixel has the smallest row index, and among those with the same smallest row index, the smallest column index.
2.  **Determine Output Dimensions:** The output grid has the same dimensions (height and width) as the target object identified in step 1.
3.  **Determine Output Color:**
    *   If the color of the target object is azure (8), the output grid is filled entirely with white (0).
    *   If the color of the target object is *not* azure (8), the output grid is filled entirely with green (3).
"""

import numpy as np

def find_target_object(grid):
    """Finds the non-background object closest to the top-left."""
    rows, cols = grid.shape
    non_background_objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                # Check if this is a new object
                is_new_object = True
                for obj in non_background_objects:
                    if (r, c) in obj['pixels']:
                        is_new_object = False
                        break
                if is_new_object:
                    # Start a new object
                    new_object = {'color': grid[r, c], 'pixels': set(), 'top_left': (r, c)}
                    # Flood fill to find all connected pixels
                    stack = [(r, c)]
                    while stack:
                        curr_r, curr_c = stack.pop()
                        if (curr_r, curr_c) not in new_object['pixels'] and 0 <= curr_r < rows and 0 <= curr_c < cols and grid[curr_r, curr_c] == new_object['color']:
                            new_object['pixels'].add((curr_r, curr_c))
                            stack.extend([(curr_r + 1, curr_c), (curr_r - 1, curr_c), (curr_r, curr_c + 1), (curr_r, curr_c - 1)])
                    non_background_objects.append(new_object)
    # Find the closest object
    if not non_background_objects:
        return None  # No non-background objects found

    closest_object = min(non_background_objects, key=lambda obj: (obj['top_left'][0], obj['top_left'][1]))

    # get dimensions
    min_r, min_c = closest_object['top_left']
    max_r = max_c = 0
    for r, c in closest_object['pixels']:
      max_r = max(max_r, r)
      max_c = max(max_c, c)

    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return closest_object['color'], height, width

def transform(input_grid):
    # initialize numpy arrays for input grid
    input_grid = np.array(input_grid)

    # Find the target object
    target_object_info = find_target_object(input_grid)

    if target_object_info is None:
      return [] #return empty list

    target_color, height, width = target_object_info

    # Initialize output_grid
    output_grid = np.zeros((height, width), dtype=int)

    # Determine output color and fill
    if target_color == 8:
        output_grid[:] = 0  # Fill with white
    else:
        output_grid[:] = 3  # Fill with green

    return output_grid.tolist()