import numpy as np

"""
Identifies two distinct non-white objects in the input grid. One object is a solid rectangle (the mask), and the other is the target object. 
The output grid preserves the mask object entirely. The target object is clipped such that only the parts that spatially overlap with the mask object's area in the input grid are retained. Pixels of the target object outside the mask area are turned white (0).
"""

def find_objects(grid):
    """
    Finds distinct contiguous objects of non-background colors.
    """
    objects = []
    visited = np.zeros(grid.shape, dtype=bool)
    rows, cols = grid.shape
    
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                
                while q:
                    row, col = q.pop(0)
                    obj_pixels.append((row, col))
                    
                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({'color': color, 'pixels': set(obj_pixels)})
                
    return objects

def is_rectangle(obj_pixels_set):
    """
    Checks if a set of pixels forms a solid rectangle.
    """
    if not obj_pixels_set:
        return False
        
    min_r = min(r for r, c in obj_pixels_set)
    max_r = max(r for r, c in obj_pixels_set)
    min_c = min(c for r, c in obj_pixels_set)
    max_c = max(c for r, c in obj_pixels_set)
    
    expected_count = (max_r - min_r + 1) * (max_c - min_c + 1)
    
    if len(obj_pixels_set) != expected_count:
        return False
        
    # Double check if all pixels within the bounds are present
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if (r, c) not in obj_pixels_set:
                return False # Should not happen if count matches, but good check
                
    return True

def transform(input_grid):
    """
    Clips one object based on the spatial extent of a rectangular mask object.
    """
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    
    # Find all non-white objects
    objects = find_objects(input_grid)
    
    # Should be exactly two objects based on examples
    if len(objects) != 2:
        # Handle unexpected cases or return input? For now, assume 2.
        # Potentially raise an error or return input if assumptions fail.
        print(f"Warning: Expected 2 objects, found {len(objects)}. Returning input.")
        return input_grid 

    # Identify the mask (rectangle) and target objects
    mask_obj = None
    target_obj = None
    
    if is_rectangle(objects[0]['pixels']):
        mask_obj = objects[0]
        target_obj = objects[1]
    elif is_rectangle(objects[1]['pixels']):
        mask_obj = objects[1]
        target_obj = objects[0]
    else:
        # Handle case where neither or both are rectangles (shouldn't happen based on examples)
        print("Warning: Could not uniquely identify a single rectangular mask object. Returning input.")
        return input_grid

    # Get the set of pixel coordinates occupied by the mask object
    mask_pixels_coords = mask_obj['pixels']
    
    # Iterate through the pixels of the target object
    for r, c in target_obj['pixels']:
        # Check if the target pixel's location is outside the mask object's area
        if (r, c) not in mask_pixels_coords:
            # If outside, change the corresponding pixel in the output grid to white (0)
            output_grid[r, c] = 0
            
    # Pixels of the mask object remain unchanged (already copied)
    # Pixels of the target object overlapping the mask remain unchanged (already copied)
    # Background pixels remain unchanged (already copied)

    return output_grid