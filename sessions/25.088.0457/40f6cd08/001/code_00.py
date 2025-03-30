import numpy as np
from collections import deque, defaultdict

"""
Identifies distinct non-background objects in the input grid.
Groups these objects based on their primary "frame" color.
For each group, identifies one object as a "template" if it contains an internal pattern (colors different from the frame color).
Identifies other objects in the same group as "targets" if they consist solely of the frame color.
Copies the internal pattern from the template object onto the corresponding internal area of each target object, respecting the target's boundaries.
The background color is white (0).
"""

def find_objects(grid):
    """
    Finds all connected components of non-background colors.
    Returns a list of objects, where each object is represented by:
    - set of pixel coordinates {(r, c), ...}
    - bounding box (min_r, min_c, max_r, max_c)
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                # Start BFS for a new object
                q = deque([(r, c)])
                visited[r, c] = True
                pixels = set([(r, c)])
                min_r, min_c, max_r, max_c = r, c, r, c
                
                while q:
                    curr_r, curr_c = q.popleft()
                    
                    # Update bounding box
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)
                    
                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            pixels.add((nr, nc))
                            q.append((nr, nc))
                            
                objects.append({
                    'pixels': pixels,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def get_object_properties(obj, grid):
    """
    Determines the frame color and whether the object has an internal pattern.
    """
    min_r, min_c, max_r, max_c = obj['bbox']
    pixels = obj['pixels']
    
    frame_colors = defaultdict(int)
    has_internal_pattern = False
    internal_pixels = set()
    
    # Check pixels on the boundary first to guess frame color
    for r, c in pixels:
        is_on_boundary = (r == min_r or r == max_r or c == min_c or c == max_c)
        if is_on_boundary:
            frame_colors[grid[r,c]] += 1
        else:
            internal_pixels.add((r,c))

    if not frame_colors: # Handle 1x1 objects or objects where all pixels are internal? This shouldn't happen with bbox definition.
        # If no clear boundary pixels (e.g., single pixel object), use the pixel's color.
        if pixels:
            r, c = next(iter(pixels))
            frame_color = grid[r, c]
        else:
            return None, False, None # Should not happen

    else:
        # Assume frame color is the most common color on the boundary
        frame_color = max(frame_colors, key=frame_colors.get)

    # Check if any internal pixel has a color different from the frame color
    pattern_details = {} # Store relative coords and colors of the pattern
    for r, c in internal_pixels:
        pixel_color = grid[r,c]
        if pixel_color != frame_color:
            has_internal_pattern = True
            dr = r - min_r
            dc = c - min_c
            pattern_details[(dr, dc)] = pixel_color
            
    # Also check boundary pixels that don't match the frame color (might be part of pattern)
    for r, c in pixels:
         is_on_boundary = (r == min_r or r == max_r or c == min_c or c == max_c)
         if is_on_boundary and grid[r,c] != frame_color:
             has_internal_pattern = True
             dr = r - min_r
             dc = c - min_c
             pattern_details[(dr, dc)] = grid[r,c]


    is_solid = not has_internal_pattern and all(grid[r,c] == frame_color for r,c in pixels)
            
    return frame_color, has_internal_pattern, is_solid, pattern_details


def transform(input_grid):
    """
    Identifies template and target objects based on frame color and internal patterns,
    then copies the pattern from the template to the targets.
    """
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find all distinct objects
    objects = find_objects(input_grid)
    
    # Group objects by potential frame color and identify templates/targets
    grouped_objects = defaultdict(lambda: {'template': None, 'targets': [], 'pattern': None})
    
    for obj in objects:
        props = get_object_properties(obj, input_grid)
        if props:
            frame_color, has_pattern, is_solid, pattern_details = props
            if frame_color is not None:
                obj_data = {'bbox': obj['bbox'], 'pixels': obj['pixels']}
                if has_pattern:
                    # Assume only one template per color group
                    if grouped_objects[frame_color]['template'] is None:
                        grouped_objects[frame_color]['template'] = obj_data
                        grouped_objects[frame_color]['pattern'] = pattern_details
                    else:
                        # Handle case with multiple patterns? For now, overwrite or ignore.
                        # Let's stick to the assumption of one template per color.
                        pass 
                elif is_solid:
                    grouped_objects[frame_color]['targets'].append(obj_data)

    # Apply patterns from templates to targets
    for frame_color, group in grouped_objects.items():
        template = group['template']
        pattern = group['pattern']
        targets = group['targets']
        
        if template and pattern and targets:
            template_min_r, template_min_c, _, _ = template['bbox']
            
            for target in targets:
                target_min_r, target_min_c, target_max_r, target_max_c = target['bbox']
                
                # Iterate through the pattern elements
                for (dr, dc), pattern_color in pattern.items():
                    # Calculate absolute position in the target
                    abs_r = target_min_r + dr
                    abs_c = target_min_c + dc
                    
                    # Check if the absolute position is within the target's bounding box
                    if target_min_r <= abs_r <= target_max_r and \
                       target_min_c <= abs_c <= target_max_c:
                        # Check if the original pixel in the target was the frame color
                        # This ensures we only overwrite the 'fill' part, not potential structure already there
                        # or parts outside the object's original pixels.
                        # Use the original input_grid for this check.
                        # Also check if the target location actually belongs to the target object pixels.
                        if (abs_r, abs_c) in target['pixels'] and input_grid[abs_r, abs_c] == frame_color:
                             output_grid[abs_r, abs_c] = pattern_color

    return output_grid.tolist() # Return as list of lists per ARC standard