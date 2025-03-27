import numpy as np

"""
Identify all distinct connected objects in the input grid.
Separate objects into two groups: 'target' objects (composed solely of azure color 8) 
and 'pattern' objects (composed of any other non-background color).
Sort both groups based on their top-left coordinate (row first, then column).
Initialize an output grid of the same size as the input, filled with the background color (white 0).
Iterate through the sorted target objects. For each target object at index 'i', 
select the pattern object at index 'i mod num_patterns'.
Copy the pixel pattern of the selected pattern object onto the output grid, 
aligning the top-left corner of the pattern with the top-left corner of the target object's original position.
Ensure copying respects grid boundaries.
"""

def find_objects(grid):
    """
    Finds all connected objects of non-background colors in the grid.

    Args:
        grid: A numpy array representing the grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains:
        'pixels': list of (row, col, color) tuples.
        'min_row', 'min_col': top-left coordinates.
        'is_target': boolean, True if the object is entirely azure (8).
        'pattern_pixels': list of (rel_row, rel_col, color) for pattern objects.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                object_pixels = []
                is_target_candidate = True
                q = [(r, c)]
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                current_object_pixels_coords = set()
                
                while q:
                    row, col = q.pop(0)
                    
                    # Check if pixel already processed for this object to handle complex shapes
                    if (row, col) in current_object_pixels_coords:
                        continue
                    current_object_pixels_coords.add((row, col))

                    px_color = grid[row, col]
                    object_pixels.append((row, col, px_color))
                    
                    if px_color != 8:
                        is_target_candidate = False # Found a non-azure color
                        
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] != 0:
                           # Check if neighbor belongs to the same object (initially, check for same color, but ARC objects can be multi-color)
                           # For this task, target objects are defined as *only* azure. Pattern objects can be multi-color.
                           # Let's assume connectivity means any non-background color adjacent.
                           visited[nr, nc] = True
                           q.append((nr, nc))
                           
                # Post-processing for the found object
                is_target = is_target_candidate # It's a target ONLY if all pixels were azure
                
                # Check if all pixels were actually azure for is_target
                if is_target:
                     for pr, pc, pcol in object_pixels:
                         if pcol != 8:
                             # This case should technically not happen if is_target_candidate logic is correct, but double-checking
                             is_target = False 
                             break

                # Calculate relative pattern pixels only if it's NOT a target
                pattern_pixels_rel = []
                if not is_target:
                    for px_r, px_c, px_col in object_pixels:
                        pattern_pixels_rel.append((px_r - min_r, px_c - min_c, px_col))
                        
                objects.append({
                    'pixels': object_pixels,
                    'min_row': min_r,
                    'min_col': min_c,
                    'is_target': is_target,
                    'pattern_pixels': pattern_pixels_rel # Only relevant for pattern objects
                })

    # Sort objects by top-left coordinate (row, then column)
    objects.sort(key=lambda obj: (obj['min_row'], obj['min_col']))
    
    return objects

def transform(input_grid):
    """
    Transforms the input grid by replacing azure objects with patterns from other objects.
    """
    rows, cols = input_grid.shape
    # Initialize output_grid with background color (0)
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find all objects in the input grid
    all_objects = find_objects(input_grid)

    # Separate objects into target (azure) and pattern objects
    target_objects = [obj for obj in all_objects if obj['is_target']]
    pattern_objects = [obj for obj in all_objects if not obj['is_target']]

    # Check if there are any patterns to use
    if not pattern_objects:
        return output_grid # Or return input_grid? Task implies replacement, so empty grid if no patterns.

    num_patterns = len(pattern_objects)

    # Iterate through sorted target objects and place corresponding patterns
    for i, target_obj in enumerate(target_objects):
        # Determine which pattern to use (cyclical)
        pattern_index = i % num_patterns
        pattern_to_use = pattern_objects[pattern_index]
        
        # Get the top-left corner where the pattern should be placed
        target_start_row = target_obj['min_row']
        target_start_col = target_obj['min_col']
        
        # Get the relative pixel data for the pattern
        pattern_pixels_rel = pattern_to_use['pattern_pixels']
        
        # "Stamp" the pattern onto the output grid
        for rel_r, rel_c, color in pattern_pixels_rel:
            output_row = target_start_row + rel_r
            output_col = target_start_col + rel_c
            
            # Ensure the pixel is within the grid bounds
            if 0 <= output_row < rows and 0 <= output_col < cols:
                output_grid[output_row, output_col] = color

    return output_grid