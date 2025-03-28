import numpy as np
from collections import deque, Counter

"""
Identifies two distinct regions in the input grid based on color composition: a 'source' and a 'target'.
1. Find all contiguous objects made of non-background (non-zero) pixels using 4-way adjacency.
2. Analyze each object: determine the colors present and their counts, and calculate the object's bounding box.
3. Identify the 'source' object: It must be the single object containing pixels of at least two different non-background colors. If zero or more than one such object exists, the transformation cannot be determined.
4. Identify potential 'target' objects: These are all objects containing pixels of only one non-background color.
5. Determine the 'pattern_color': This is the least frequent non-background color within the identified 'source' object.
6. Select the final 'target' object: From the potential candidates, choose the one whose single color is *different* from the 'pattern_color'. If multiple candidates satisfy this, or none do, the transformation cannot be determined definitively (though this case might need refinement based on more examples). Assume only one valid target exists.
7. Determine the 'target_color': This is the single color of the selected 'target' object.
8. Map the pattern: Find the relative coordinates (row, col offsets from the top-left corner) of all pixels matching the 'pattern_color' *within the bounding box* of the 'source' object.
9. Apply the pattern: For each relative coordinate derived in the previous step, calculate the corresponding absolute coordinate within the 'target' object's bounding box (by adding the offset to the target's top-left corner).
10. Update the output grid: If the calculated target coordinate is within the grid bounds and the pixel at that location in the *input* grid has the 'target_color', change the color of the corresponding pixel in the *output* grid to the 'pattern_color'. Otherwise, leave the pixel unchanged.
11. All other pixels in the output grid remain the same as the input grid.
"""

def find_objects(grid, ignore_color=0):
    """
    Finds contiguous objects of non-ignored colors in the grid.
    An object is a set of connected pixels (4-way adjacency) of any non-ignored color.

    Args:
        grid (np.array): The input grid.
        ignore_color (int): The color to ignore (usually background 0).

    Returns:
        list: A list of dictionaries, where each dict represents an object
              and contains 'pixels' (a set of (r, c) tuples).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != ignore_color and not visited[r, c]:
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if neighbor is not visited and not ignored color
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] != ignore_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if obj_pixels:
                    objects.append({'pixels': obj_pixels})
                    
    return objects

def get_bounding_box(pixels):
    """
    Calculates the bounding box for a set of pixels.

    Args:
        pixels (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if pixels is empty.
    """
    if not pixels:
        return None
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    return min(rows), min(cols), max(rows), max(cols)

def analyze_object_properties(grid, obj):
    """
    Analyzes the colors present within an object's pixels and finds its bounding box.
    Adds 'colors_in_pixels' (Counter) and 'bbox' to the object dict.
    """
    colors = Counter()
    for r, c in obj['pixels']:
        colors[grid[r, c]] += 1
    obj['colors_in_pixels'] = colors
    obj['bbox'] = get_bounding_box(obj['pixels'])


def transform(input_grid):
    """
    Applies the pattern transfer transformation based on source/target object identification.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # 1. Find all distinct contiguous objects (ignoring background color 0)
    objects = find_objects(input_grid, ignore_color=0)
    
    # 2. Analyze colors and bounding box for each object
    for obj in objects:
        analyze_object_properties(input_grid, obj)
        
    # 3. Identify source object (must be unique object with >1 color)
    source_object = None
    source_candidates = [obj for obj in objects if len(obj['colors_in_pixels']) > 1]
    if len(source_candidates) == 1:
        source_object = source_candidates[0]
    else:
        # If 0 or >1 multi-color objects found, cannot proceed with this logic
        # print(f"Warning: Found {len(source_candidates)} source candidates. Expected 1. Returning input.")
        return output_grid 

    # 4. Identify potential target objects (exactly 1 color)
    target_candidates = [obj for obj in objects if len(obj['colors_in_pixels']) == 1]
    
    if not target_candidates:
        # print("Warning: No target candidates found. Returning input.")
        return output_grid

    # 5. Determine pattern color (least frequent non-background in source)
    # Ensure colors_in_pixels is not empty (already guaranteed by source selection criteria)
    pattern_color = min(source_object['colors_in_pixels'], key=source_object['colors_in_pixels'].get)

    # 6. Select the actual target object (single color, different from pattern color)
    final_target_object = None
    valid_targets = []
    for obj in target_candidates:
        target_candidate_color = list(obj['colors_in_pixels'].keys())[0]
        if target_candidate_color != pattern_color:
            valid_targets.append(obj)
            
    if len(valid_targets) == 1:
        final_target_object = valid_targets[0]
    else:
        # If 0 or >1 valid targets found based on color rule, cannot proceed
        # print(f"Warning: Found {len(valid_targets)} valid target candidates (color != pattern_color). Expected 1. Returning input.")
        return output_grid
        
    # 7. Determine target color
    target_color = list(final_target_object['colors_in_pixels'].keys())[0] 
    
    # 8. Get bounding boxes
    src_r1, src_c1, src_r2, src_c2 = source_object['bbox']
    tgt_r1, tgt_c1, tgt_r2, tgt_c2 = final_target_object['bbox']

    # 9. Find relative coordinates of pattern pixels within the source bounding box
    pattern_relative_coords = []
    for r in range(src_r1, src_r2 + 1):
        for c in range(src_c1, src_c2 + 1):
             # Check the input_grid value at (r,c) within the source bbox
             if 0 <= r < rows and 0 <= c < cols and input_grid[r, c] == pattern_color:
                 rel_r = r - src_r1
                 rel_c = c - src_c1
                 pattern_relative_coords.append((rel_r, rel_c))

    # 10. Apply pattern to target object in output grid
    for rel_r, rel_c in pattern_relative_coords:
        # Calculate corresponding target coordinates
        tgt_r = tgt_r1 + rel_r
        tgt_c = tgt_c1 + rel_c
        
        # 11. Update output grid if conditions met
        # Check if target coordinates are within grid bounds
        if 0 <= tgt_r < rows and 0 <= tgt_c < cols:
            # Check if the pixel at the target location in the *input* grid had the target_color
            if input_grid[tgt_r, tgt_c] == target_color:
                # Update the output grid
                output_grid[tgt_r, tgt_c] = pattern_color

    return output_grid