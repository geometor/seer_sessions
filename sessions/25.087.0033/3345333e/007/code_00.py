import numpy as np
from collections import deque, Counter

"""
The transformation rule identifies two potential target objects for removal:
1. 'unique_solid': An object that is the only one of its color AND is a solid rectangle.
2. 'majority_largest': The largest object (by pixel area) belonging to the color group that has the most distinct objects. Ties in object count are broken by selecting the color with the largest total pixel area.

The default action is to remove 'unique_solid' if exactly one such object exists.

However, this action is overridden, and 'majority_largest' is removed instead, IF ALL of the following conditions are met:
- Both 'unique_solid' and 'majority_largest' exist.
- 'majority_largest' is NOT a solid rectangle.
- The area of 'majority_largest' is greater than the area of 'unique_solid'.
- The difference in area between 'majority_largest' and 'unique_solid' is greater than 10 pixels.

If 'unique_solid' does not exist, but 'majority_largest' does, then 'majority_largest' is removed.

If neither 'unique_solid' nor 'majority_largest' can be definitively identified according to these rules, the grid remains unchanged. Removal consists of changing the object's pixels to the background color (white, 0).
"""

# === Helper Functions ===

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-background color in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary contains:
              {'color': int, 'coords': set((r, c)), 'size': int, 'bbox': dict}.
              bbox is {'min_r', 'max_r', 'min_c', 'max_c'}. Returns empty list if no objects.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # If pixel is non-background (not 0) and not visited yet
            if color != 0 and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_color = color 
                min_r, max_r = r, r
                min_c, max_c = c, c
                
                # Breadth-First Search (BFS) to find connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == obj_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if obj_coords:
                    bbox = {'min_r': min_r, 'max_r': max_r, 'min_c': min_c, 'max_c': max_c}
                    objects.append({
                        'color': int(obj_color), 
                        'coords': obj_coords, 
                        'size': len(obj_coords), 
                        'bbox': bbox
                    }) 
                    
    return objects

def is_solid_rectangle(obj):
    """
    Checks if an object (represented by its dictionary) is a solid rectangle.

    Args:
        obj (dict): The object dictionary from find_objects.

    Returns:
        bool: True if the object is a solid rectangle, False otherwise.
    """
    coords = obj['coords']
    if not coords:
        return False
        
    bbox = obj['bbox']
    height = bbox['max_r'] - bbox['min_r'] + 1
    width = bbox['max_c'] - bbox['min_c'] + 1
    
    # Check if the number of pixels in the object equals the area of its bounding box
    return obj['size'] == height * width

# === Main Transformation Function ===

def transform(input_grid):
    """
    Applies the transformation rule based on 'unique_solid' and 'majority_largest' objects.
    """
    output_grid = np.copy(input_grid)
    
    # 1. Find all objects
    objects = find_objects(input_grid)
    if not objects:
        return output_grid # No objects, return original grid

    # 2. Identify 'unique_solid'
    color_counts = Counter(obj['color'] for obj in objects)
    num_objects_by_color = {int(k): int(v) for k, v in color_counts.items()}
    
    unique_solid_object = None
    unique_solid_found = False
    for obj in objects:
        obj['is_solid'] = is_solid_rectangle(obj) # Cache solidity check
        if num_objects_by_color[obj['color']] == 1 and obj['is_solid']:
            if unique_solid_found: # Found more than one
                unique_solid_object = None
                break 
            else:
                 unique_solid_object = obj
                 unique_solid_found = True
    # Ensure unique_solid_object is None if multiple were found
    if unique_solid_object is not None and not unique_solid_found:
         unique_solid_object = None


    # 3. Identify 'majority_largest'
    majority_color = -1
    majority_largest_object = None
    
    if num_objects_by_color:
        max_count = 0
        # Check if there are any colors with multiple objects
        if any(v > 1 for v in num_objects_by_color.values()):
             max_count = max(num_objects_by_color.values())
        elif num_objects_by_color: # If no color has >1 object, consider max count as 1
            max_count = 1 
            
        if max_count > 0: # Proceed only if there are objects
            majority_colors = [color for color, count in num_objects_by_color.items() if count == max_count]
            
            if len(majority_colors) == 1:
                majority_color = majority_colors[0]
            elif len(majority_colors) > 1: # Tie-break by total area
                max_total_area = -1
                chosen_color = -1
                for color in majority_colors:
                    total_area = sum(obj['size'] for obj in objects if obj['color'] == color)
                    if total_area > max_total_area:
                        max_total_area = total_area
                        chosen_color = color
                majority_color = chosen_color

            # Find the largest object of the majority color
            if majority_color != -1:
                largest_size = -1
                for obj in objects:
                    if obj['color'] == majority_color:
                        # Solidity was already calculated and cached in step 2
                        # obj['is_solid'] = is_solid_rectangle(obj) 
                        if obj['size'] > largest_size:
                            largest_size = obj['size']
                            majority_largest_object = obj

    # 4. Apply Decision Logic
    target_object_to_remove = None
    
    # Primary Rule
    if unique_solid_object is not None:
        target_object_to_remove = unique_solid_object
        
        # Override Check
        if majority_largest_object is not None:
            # Ensure solidity is checked for majority_largest if not already done
            if 'is_solid' not in majority_largest_object:
                 majority_largest_object['is_solid'] = is_solid_rectangle(majority_largest_object)

            override_conditions_met = (
                not majority_largest_object['is_solid'] and
                majority_largest_object['size'] > unique_solid_object['size'] and
                (majority_largest_object['size'] - unique_solid_object['size']) > 10
            )
            
            if override_conditions_met:
                target_object_to_remove = majority_largest_object # Override target

    # Fallback: If no unique_solid, but majority_largest exists
    elif majority_largest_object is not None:
         target_object_to_remove = majority_largest_object

    # 5. Execute Removal
    if target_object_to_remove is not None:
        for r, c in target_object_to_remove['coords']:
             # Basic bounds check (should be redundant)
            if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                 output_grid[r, c] = 0 # Set to background color

    # 6. Return the resulting grid
    return output_grid