"""
Determine the dimensions of a uniform white output grid based on properties of specific objects within the input grid.

1.  Scan the input grid to find all distinct groups of connected, non-background pixels (objects).
2.  For each object, determine its color (C) and calculate the height (H) and width (W) of its bounding box.
3.  Identify the unique object where its color value C equals its bounding box height H. Record its bounding box width (W_target).
4.  Identify the object with the minimum color value C among all objects. Record its bounding box height (H_min).
5.  Create a new grid with dimensions H_min rows and W_target columns.
6.  Fill this new grid entirely with the background color (0).
"""

import numpy as np
from collections import defaultdict

def find_objects(grid):
    """
    Identifies connected components (objects) of the same non-background color.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A dictionary where keys are colors (1-9) and values are lists of
        lists of (row, col) coordinates for each object of that color.
        e.g., {color: [[(r1, c1), (r2, c2), ...], [(r3, c3), ...]]}
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects_by_color = defaultdict(list)

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # If not background and not visited yet, start a flood fill
            if color != 0 and not visited[r, c]:
                object_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                
                while q:
                    row, col = q.pop(0)
                    object_pixels.append((row, col))
                    
                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if object_pixels:
                     objects_by_color[color].append(object_pixels)

    return objects_by_color


def get_bounding_box(pixels):
    """
    Calculates the bounding box for a set of pixels.

    Args:
        pixels: A list of (row, col) coordinates for an object.

    Returns:
        A tuple (min_row, max_row, min_col, max_col).
    """
    if not pixels:
        return None
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    return min(rows), max(rows), min(cols), max(cols)

def get_object_properties(grid):
    """
    Finds all objects and calculates their properties (color, height, width).

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, each representing an object with keys:
        'color', 'height', 'width', 'pixels'.
    """
    objects_data = []
    objects_by_color = find_objects(grid)

    for color, object_list in objects_by_color.items():
        for pixels in object_list:
            if not pixels:
                continue
            min_r, max_r, min_c, max_c = get_bounding_box(pixels)
            height = max_r - min_r + 1
            width = max_c - min_c + 1
            objects_data.append({
                'color': color,
                'height': height,
                'width': width,
                'pixels': pixels # Store pixels if needed later, though not for this task
            })
    return objects_data


def transform(input_grid_list):
    """
    Transforms the input grid according to the identified rules.

    Args:
        input_grid_list: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    input_grid = np.array(input_grid_list, dtype=int)

    # Step 1 & 2: Find objects and calculate their properties
    all_objects = get_object_properties(input_grid)

    if not all_objects:
         # Handle cases with no colored objects (though unlikely based on examples)
         # Return a minimal 1x1 white grid as a default? Or raise error?
         # Based on examples, there will always be objects. Let's assume this.
         # If needed, add specific error handling or default output.
         # For now, let's proceed assuming objects exist.
         print("Warning: No objects found in the input grid.")
         return [[0]] 


    # Step 3: Find the height-matched object and its width (W_target)
    w_target = None
    height_matched_object_found = False
    for obj in all_objects:
        if obj['color'] == obj['height']:
             # Ensure uniqueness if multiple matches exist (task implies unique)
            if height_matched_object_found:
                 # Handle ambiguity if needed - perhaps raise error or use first match?
                 # For now, assume uniqueness as per analysis.
                 print(f"Warning: Multiple height-matched objects found. Using the first one with color {obj['color']}.")
                 pass # Continue using the first found w_target
            else:
                w_target = obj['width']
                height_matched_object_found = True
                # We could break here if we are certain it's unique

    # Step 4: Find the min-color object and its height (H_min)
    min_color = float('inf')
    h_min = None
    for obj in all_objects:
        if obj['color'] < min_color:
            min_color = obj['color']
            h_min = obj['height']
        # If multiple objects share the minimum color, the task description doesn't specify tie-breaking.
        # Current logic takes the height of the *first* object encountered with the minimum color.
        # Re-evaluate if examples show different tie-breaking needed.


    # Error handling if key objects weren't found
    if w_target is None:
        raise ValueError("Could not find a height-matched object (color == height).")
    if h_min is None:
         # This should technically not happen if all_objects is not empty
        raise ValueError("Could not determine the minimum color object's height.")


    # Step 5 & 6: Create and fill the output grid
    output_grid = np.zeros((h_min, w_target), dtype=int)

    return output_grid.tolist()