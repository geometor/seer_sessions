import numpy as np
from collections import deque, defaultdict

"""
Transformation Rule:
1. Find all distinct connected objects (contiguous non-white pixels) in the input grid.
2. For each object, determine its 'frame' color. The frame color is defined as the most frequent color among the object's pixels that are adjacent (4-connectivity) to the background (white, color 0). If an object has no pixels adjacent to the background or is a single pixel, its frame color is simply its most frequent color (or its only color).
3. Identify objects that contain an 'internal pattern'. An internal pattern consists of all pixels within the object whose color is *different* from the object's frame color. Store this pattern as a dictionary mapping relative coordinates (dr, dc) from the object's top-left corner to the pattern color. An object with such a pattern is a 'template'.
4. Identify objects that are 'solid'. A solid object consists entirely of pixels of its frame color (i.e., it has no internal pattern). These are 'targets'.
5. Group objects by their frame color. Within each group, there should ideally be one template object and one or more target objects.
6. For each group with a template and targets:
    a. Get the pattern from the template object.
    b. For each target object in the group:
        i. Iterate through the template's pattern elements `{(dr, dc): pattern_color}`.
        ii. Calculate the corresponding absolute coordinates `(abs_r, abs_c)` within the target's bounding box: `abs_r = target_min_r + dr`, `abs_c = target_min_c + dc`.
        iii. Check if the calculated coordinate `(abs_r, abs_c)` exists within the *original set of pixels* defining the target object.
        iv. If it does, change the color of the pixel at `(abs_r, abs_c)` in the output grid to `pattern_color`. This effectively copies the pattern onto the target, constrained by the target's shape.
7. The output grid is the initial grid modified by applying the patterns to the corresponding targets.
"""

def find_objects(grid):
    """
    Finds all connected components of non-background colors using BFS.
    Args:
        grid (np.array): Input grid.
    Returns:
        list: A list of objects, where each object is a dictionary containing:
            - 'pixels': A set of (row, col) tuples belonging to the object.
            - 'bbox': A tuple (min_r, min_c, max_r, max_c) representing the bounding box.
            - 'colors': A defaultdict counting the occurrences of each color in the object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                q = deque([(r, c)])
                visited[r, c] = True
                pixels = set([(r, c)])
                min_r, min_c, max_r, max_c = r, c, r, c
                obj_colors = defaultdict(int)
                obj_colors[color] += 1
                
                while q:
                    curr_r, curr_c = q.popleft()
                    
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
                            obj_colors[grid[nr, nc]] += 1
                            
                objects.append({
                    'pixels': pixels,
                    'bbox': (min_r, min_c, max_r, max_c),
                    'colors': obj_colors
                })
    return objects

def get_object_properties(obj, grid):
    """
    Determines the frame color, internal pattern, and solidity of an object.
    Args:
        obj (dict): An object dictionary from find_objects.
        grid (np.array): The input grid.
    Returns:
        tuple: (frame_color, has_internal_pattern, is_solid, pattern_details)
               pattern_details is a dict {(dr, dc): color} or None if no pattern.
               Returns (None, False, False, None) if properties cannot be determined.
    """
    pixels = obj['pixels']
    min_r, min_c, max_r, max_c = obj['bbox']
    obj_colors = obj['colors']
    rows, cols = grid.shape
    
    if not pixels:
        return None, False, False, None

    # Determine frame color: most frequent color adjacent to background (0)
    adjacent_to_bg_colors = defaultdict(int)
    has_adjacent_to_bg = False
    for r, c in pixels:
        is_adj_to_bg = False
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr, nc] == 0:
                is_adj_to_bg = True
                break
        if is_adj_to_bg:
            adjacent_to_bg_colors[grid[r, c]] += 1
            has_adjacent_to_bg = True

    if has_adjacent_to_bg:
        # Frame color is the most frequent among those adjacent to background
        frame_color = max(adjacent_to_bg_colors, key=adjacent_to_bg_colors.get)
    elif obj_colors:
        # Fallback: most frequent color overall if no pixel is adjacent to background
        # Or if it's a single pixel object
         frame_color = max(obj_colors, key=obj_colors.get)
    else:
        # Should not happen if pixels is not empty
        return None, False, False, None 

    # Extract internal pattern (pixels with color != frame_color)
    pattern_details = {}
    for r, c in pixels:
        pixel_color = grid[r, c]
        if pixel_color != frame_color:
            dr = r - min_r
            dc = c - min_c
            pattern_details[(dr, dc)] = pixel_color
            
    has_internal_pattern = bool(pattern_details)
    is_solid = not has_internal_pattern
            
    return frame_color, has_internal_pattern, is_solid, pattern_details


def transform(input_grid_list):
    """
    Transforms the input grid based on the described pattern transfer logic.
    Args:
        input_grid_list (list): A list of lists representing the input grid.
    Returns:
        list: A list of lists representing the transformed output grid.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.copy(input_grid)
    
    # 1. Find all distinct objects
    objects = find_objects(input_grid)
    
    # 2. Group objects by frame color and identify templates/targets
    grouped_objects = defaultdict(lambda: {'template': None, 'targets': [], 'pattern': None})
    
    for obj in objects:
        # 3. Determine properties for each object
        props = get_object_properties(obj, input_grid)
        if props:
            frame_color, has_pattern, is_solid, pattern_details = props
            
            if frame_color is not None:
                obj_data = {'bbox': obj['bbox'], 'pixels': obj['pixels']}
                
                # 4. Classify as template or target
                if has_pattern:
                    # Assume only one template per color group for simplicity
                    if grouped_objects[frame_color]['template'] is None:
                        grouped_objects[frame_color]['template'] = obj_data
                        grouped_objects[frame_color]['pattern'] = pattern_details
                    else:
                        # Handle multiple potential templates if needed (e.g., pick largest, first found?)
                        # Current logic: keep the first one found.
                        pass 
                elif is_solid:
                    # Object is solid frame color -> target
                    grouped_objects[frame_color]['targets'].append(obj_data)

    # 5. & 6. Apply patterns from templates to targets within each group
    for frame_color, group in grouped_objects.items():
        template = group['template']
        pattern = group['pattern']
        targets = group['targets']
        
        if template and pattern and targets:
            # Template exists, has a pattern, and there are targets of the same frame color
            
            for target in targets:
                target_min_r, target_min_c, _, _ = target['bbox']
                target_pixels = target['pixels'] # The set of actual pixels in the target

                # Iterate through the pattern elements extracted from the template
                for (dr, dc), pattern_color in pattern.items():
                    # Calculate the absolute position where this pattern pixel should go in the target
                    abs_r = target_min_r + dr
                    abs_c = target_min_c + dc
                    
                    # Crucial check: Apply pattern color *only if* the target position (abs_r, abs_c)
                    # corresponds to an actual pixel within the target object's original shape.
                    if (abs_r, abs_c) in target_pixels:
                         # Since the target was identified as solid, input_grid[abs_r, abs_c] == frame_color.
                         # Update the output grid at this position.
                         output_grid[abs_r, abs_c] = pattern_color

    # 7. Return the modified grid as a list of lists
    return output_grid.tolist() 