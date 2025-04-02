```python
import numpy as np
from collections import deque

"""
Identifies distinct non-background colored objects in the input grid.
Determines if the objects are arranged primarily horizontally or vertically.
If arranged horizontally, reorders the objects based on their width (ascending) while preserving horizontal spacing and vertical alignment.
If arranged vertically, reverses the vertical order of the objects while preserving vertical spacing and horizontal alignment.
Reconstructs the output grid with the reordered objects.
"""

def find_objects(grid):
    """
    Finds all connected components of non-background colors in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of tuples, where each tuple represents an object:
              (color, set_of_coordinates, bounding_box)
              bounding_box is (min_r, min_c, max_r, max_c)
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    background_color = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    coords.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                bounding_box = (min_r, min_c, max_r, max_c)
                objects.append({'color': color, 'coords': coords, 'bbox': bounding_box})

    return objects

def determine_layout_and_order(objects):
    """
    Determines the layout (horizontal/vertical) and calculates spacing.
    Sorts objects initially by position (top-left).

    Args:
        objects (list): List of object dictionaries.

    Returns:
        tuple: (layout_axis, sorted_original_objects, separation)
               layout_axis is 'horizontal' or 'vertical' or 'unknown'.
               sorted_original_objects is the list sorted by position.
               separation is the average gap size (int). Returns 0 if layout unclear or < 2 objects.
    """
    if not objects:
        return 'unknown', [], 0
    
    # Sort objects by top-left corner (row first, then column)
    objects.sort(key=lambda o: (o['bbox'][0], o['bbox'][1]))

    if len(objects) < 2:
        return 'unknown', objects, 0 # Layout needs at least 2 objects to be meaningful

    # Check for horizontal layout
    is_horizontal = True
    horizontal_gaps = []
    for i in range(len(objects) - 1):
        o1 = objects[i]
        o2 = objects[i+1]
        min_r1, min_c1, max_r1, max_c1 = o1['bbox']
        min_r2, min_c2, max_r2, max_c2 = o2['bbox']
        
        # Check if o2 is to the right of o1
        if min_c2 > max_c1:
             # Check vertical overlap (at least one row must overlap)
             overlap_start = max(min_r1, min_r2)
             overlap_end = min(max_r1, max_r2)
             if overlap_end >= overlap_start:
                 horizontal_gaps.append(min_c2 - max_c1 - 1)
             else:
                 is_horizontal = False
                 break
        else:
            is_horizontal = False
            break
            
    if is_horizontal and horizontal_gaps:
        separation = round(sum(horizontal_gaps) / len(horizontal_gaps))
        return 'horizontal', objects, int(separation)

    # Check for vertical layout (reset sort order check based on vertical position)
    # Re-sort based on column first might be needed if horizontal alignment is strict
    # For now, assume the initial row-then-col sort is sufficient for vertical stacking check too.
    is_vertical = True
    vertical_gaps = []
    for i in range(len(objects) - 1):
        o1 = objects[i]
        o2 = objects[i+1]
        min_r1, min_c1, max_r1, max_c1 = o1['bbox']
        min_r2, min_c2, max_r2, max_c2 = o2['bbox']

        # Check if o2 is below o1
        if min_r2 > max_r1:
            # Check horizontal overlap (at least one column must overlap)
            overlap_start = max(min_c1, min_c2)
            overlap_end = min(max_c1, max_c2)
            if overlap_end >= overlap_start:
                vertical_gaps.append(min_r2 - max_r1 - 1)
            else:
                # This case might occur if objects are staggered vertically AND horizontally
                # Let's assume for now pure vertical implies good horizontal overlap
                 is_vertical = False
                 break
        else:
            # This could be side-by-side or overlapping, not purely vertical stacking
             is_vertical = False
             break
             
    if is_vertical and vertical_gaps:
        separation = round(sum(vertical_gaps) / len(vertical_gaps))
        return 'vertical', objects, int(separation)

    # If neither clearly horizontal nor vertical based on sequence
    return 'unknown', objects, 0


def transform(input_grid):
    """
    Transforms the input grid by reordering objects based on layout.
    Horizontal layout: sort by width (ascending).
    Vertical layout: reverse order.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    output_grid = np.zeros_like(input_grid_np, dtype=int) # Initialize with background color 0
    
    # --- Step 1: Identify Objects ---
    objects = find_objects(input_grid_np)
    
    if not objects:
        return output_grid.tolist() # Return empty grid if no objects

    # --- Step 2: Determine Layout and Original Order ---
    layout_axis, original_ordered_objects, separation = determine_layout_and_order(objects)

    if layout_axis == 'unknown' or len(objects) < 2:
        # If layout is unclear or only one object, return the original grid (or as identified)
        # We'll place the single object back for robustness
         if objects:
             obj = objects[0]
             for r, c in obj['coords']:
                  if 0 <= r < rows and 0 <= c < cols:
                      output_grid[r, c] = obj['color']
         return output_grid.tolist()


    # --- Step 3: Apply Reordering Rule ---
    if layout_axis == 'horizontal':
        # Calculate width for sorting
        for obj in objects:
            min_r, min_c, max_r, max_c = obj['bbox']
            obj['width'] = max_c - min_c + 1
        # Sort by width
        reordered_objects = sorted(objects, key=lambda o: o['width'])
        
        # --- Step 4: Reconstruct Grid (Horizontal) ---
        # Find the starting column of the first object in the *original* sequence
        start_col = min(o['bbox'][1] for o in original_ordered_objects)
        current_col = start_col
        
        for obj in reordered_objects:
            color = obj['color']
            min_r_orig, min_c_orig, _, _ = obj['bbox']
            # Place object relative to current_col and its original min_r
            for r, c in obj['coords']:
                # Calculate offset: how far each pixel is from the object's original top-left
                offset_r = r - min_r_orig
                offset_c = c - min_c_orig
                # Calculate new position
                new_r = min_r_orig + offset_r # Keep original row position
                new_c = current_col + offset_c
                if 0 <= new_r < rows and 0 <= new_c < cols:
                    output_grid[new_r, new_c] = color
            
            # Update current_col for the next object
            obj_width = obj['width'] # Use calculated width
            current_col += obj_width + separation

    elif layout_axis == 'vertical':
        # Reverse the order (original_ordered_objects is already sorted by position)
        reordered_objects = original_ordered_objects[::-1]

        # --- Step 4: Reconstruct Grid (Vertical) ---
        # Find the starting row of the first object in the *original* sequence
        start_row = min(o['bbox'][0] for o in original_ordered_objects)
        current_row = start_row

        for obj in reordered_objects:
            color = obj['color']
            min_r_orig, min_c_orig, max_r_orig, _ = obj['bbox']
            obj_height = max_r_orig - min_r_orig + 1

            # Place object relative to current_row and its original min_c
            for r, c in obj['coords']:
                 # Calculate offset: how far each pixel is from the object's original top-left
                offset_r = r - min_r_orig
                offset_c = c - min_c_orig
                # Calculate new position
                new_r = current_row + offset_r
                new_c = min_c_orig + offset_c # Keep original col position
                if 0 <= new_r < rows and 0 <= new_c < cols:
                    output_grid[new_r, new_c] = color
            
            # Update current_row for the next object
            current_row += obj_height + separation
            
    return output_grid.tolist()

```