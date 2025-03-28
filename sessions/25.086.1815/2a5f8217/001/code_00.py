import numpy as np
from collections import deque

"""
Identifies all distinct, connected objects (non-white pixels) in the input grid.
Separates objects into blue objects (color 1) and non-blue objects (other non-white colors).
Creates a mapping from object shape to color based on the non-blue objects. If multiple non-blue objects share the same shape, the color of the object whose top-left corner appears latest in a top-to-bottom, left-to-right scan is used.
Iterates through the blue objects. If a blue object's shape matches a shape in the mapping, the blue object is assigned the corresponding color. Both the blue object and the shape entry are marked as used.
If exactly one blue object remains unassigned and exactly one color from the original set of non-blue object colors remains unused after the shape-matching step, the remaining blue object is assigned the remaining unused color.
Creates the output grid by copying the input grid and changing the color of the pixels belonging to the assigned blue objects to their newly assigned colors.
"""

def find_objects(grid):
    """
    Finds all connected objects of the same color in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each representing an object with keys:
              'pixels': set of (row, col) tuples for the object's pixels.
              'color': the color of the object.
              'top_left': the (row, col) tuple of the top-leftmost pixel.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and not visited[r, c]:
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c

                while q:
                    curr_r, curr_c = q.popleft()
                    obj_pixels.add((curr_r, curr_c))
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = curr_r + dr, curr_c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                objects.append({'pixels': obj_pixels, 'color': color, 'top_left': (min_r, min_c)})
                
    return objects

def get_shape(pixels):
    """
    Calculates a canonical shape representation for an object.

    Args:
        pixels (set): A set of (row, col) tuples for the object's pixels.

    Returns:
        tuple: A sorted tuple of (row, col) tuples representing the shape,
               normalized relative to the top-left corner. Returns None if pixels is empty.
    """
    if not pixels:
        return None
        
    min_r = min(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    
    # Normalize coordinates relative to the top-left corner
    shape_coords = tuple(sorted([(r - min_r, c - min_c) for r, c in pixels]))
    return shape_coords


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Find all objects in the input grid
    all_objects = find_objects(np.array(input_grid))

    # Separate objects into blue and non-blue
    blue_objects = []
    non_blue_objects = []
    for obj in all_objects:
        obj['shape'] = get_shape(obj['pixels']) # Add shape representation
        if obj['color'] == 1:
            blue_objects.append(obj)
        elif obj['color'] != 0:
            non_blue_objects.append(obj)

    # Sort non-blue objects by top-left corner (top-to-bottom, left-to-right)
    non_blue_objects.sort(key=lambda o: (o['top_left'][0], o['top_left'][1]))

    # Create the shape-to-color map from non-blue objects
    shape_to_color_map = {}
    available_non_blue_colors = set()
    for obj in non_blue_objects:
        shape_to_color_map[obj['shape']] = obj['color']
        available_non_blue_colors.add(obj['color'])

    # Perform shape matching
    recolor_assignments = {} # Map from original blue object index to new color
    unhandled_blue_indices = list(range(len(blue_objects)))
    used_shapes = set()
    used_colors = set()

    for i in unhandled_blue_indices[:]: # Iterate over a copy for safe removal
        blue_obj = blue_objects[i]
        blue_shape = blue_obj['shape']
        if blue_shape in shape_to_color_map and blue_shape not in used_shapes:
            target_color = shape_to_color_map[blue_shape]
            # Check if this target color derived from this shape is already used by another match
            # Find the non-blue object that provided this color for this shape
            provider_obj = None
            for nb_obj in reversed(non_blue_objects): # Check in reverse to find the last one
                if nb_obj['shape'] == blue_shape:
                    provider_obj = nb_obj
                    break
            
            # Ensure the *specific instance* of the shape/color pair hasn't been conceptually 'used'
            # In this logic, shape uniqueness is the primary key. If a shape matches, we use its associated color.
            # We need to track which shapes from the map have been used.
            
            recolor_assignments[i] = target_color
            unhandled_blue_indices.remove(i)
            used_shapes.add(blue_shape)
            used_colors.add(target_color) # Track which colors got assigned

    # Handle the remainder case
    remaining_blue_indices = unhandled_blue_indices
    unused_colors = available_non_blue_colors - used_colors

    if len(remaining_blue_indices) == 1 and len(unused_colors) == 1:
        remaining_blue_idx = remaining_blue_indices[0]
        remaining_color = list(unused_colors)[0]
        recolor_assignments[remaining_blue_idx] = remaining_color
        # No need to remove from remaining_blue_indices as we won't iterate further

    # Create the output grid and apply recoloring
    output_grid = np.array(input_grid).copy()
    for blue_idx, new_color in recolor_assignments.items():
        blue_obj = blue_objects[blue_idx]
        for r, c in blue_obj['pixels']:
            output_grid[r, c] = new_color

    return output_grid.tolist()