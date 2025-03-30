import numpy as np
from collections import defaultdict, deque
import itertools

"""
Identifies all distinct non-white objects in the input grid. 
For each color, it considers all pairs of objects of that color. 
If a pair of objects is aligned either horizontally or vertically, 
and the rectangular area directly between them consists entirely of white pixels (0), 
that area is filled with azure pixels (8) in the output grid. 
The original objects remain unchanged.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-white color.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains 'color', 'coords' (a set of (row, col) tuples), 
        and 'bbox' (a tuple: min_row, max_row, min_col, max_col).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c
                
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)
                    
                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({
                    'color': color,
                    'coords': obj_coords,
                    'bbox': (min_r, max_r, min_c, max_c)
                })
    return objects

def transform(input_grid):
    """
    Transforms the input grid by filling white gaps between same-colored objects
    with azure pixels.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Find all non-white objects
    objects = find_objects(input_grid)
    
    # Group objects by color
    objects_by_color = defaultdict(list)
    for obj in objects:
        objects_by_color[obj['color']].append(obj)
        
    # Iterate through each color group with 2 or more objects
    for color, group in objects_by_color.items():
        if len(group) < 2:
            continue
            
        # Iterate through all unique pairs of objects of the same color
        for obj1, obj2 in itertools.combinations(group, 2):
            bbox1 = obj1['bbox']
            bbox2 = obj2['bbox']
            
            # Ensure object 1 is consistently "first" (leftmost or topmost)
            # This simplifies gap calculation logic
            if bbox1[2] > bbox2[2]: # obj1 is right of obj2
                obj1, obj2 = obj2, obj1
                bbox1, bbox2 = bbox2, bbox1
            elif bbox1[2] == bbox2[2] and bbox1[0] > bbox2[0]: # Same column start, obj1 below obj2
                obj1, obj2 = obj2, obj1
                bbox1, bbox2 = bbox2, bbox1

            r1_min, r1_max, c1_min, c1_max = bbox1
            r2_min, r2_max, c2_min, c2_max = bbox2

            # --- Horizontal Check ---
            # Check for row overlap
            overlap_r_min = max(r1_min, r2_min)
            overlap_r_max = min(r1_max, r2_max)
            
            if overlap_r_min <= overlap_r_max:
                # Define potential horizontal gap columns
                gap_c_min = c1_max + 1
                gap_c_max = c2_min - 1
                
                if gap_c_min <= gap_c_max:
                    # Check if the gap area is entirely white
                    gap_area = input_grid[overlap_r_min : overlap_r_max + 1, gap_c_min : gap_c_max + 1]
                    if np.all(gap_area == 0):
                        # Fill the gap with azure (8)
                        output_grid[overlap_r_min : overlap_r_max + 1, gap_c_min : gap_c_max + 1] = 8
                        
            # --- Vertical Check ---
            # Check for column overlap
            overlap_c_min = max(c1_min, c2_min)
            overlap_c_max = min(c1_max, c2_max)

            if overlap_c_min <= overlap_c_max:
                 # Define potential vertical gap rows (ensure obj1 is above obj2 for this check)
                 # Re-assign temporarily if needed just for vertical check logic
                 temp_obj1, temp_obj2 = obj1, obj2
                 temp_bbox1, temp_bbox2 = bbox1, bbox2
                 if temp_bbox1[0] > temp_bbox2[0]: # obj1 is below obj2
                     temp_obj1, temp_obj2 = temp_obj2, temp_obj1
                     temp_bbox1, temp_bbox2 = temp_bbox2, temp_bbox1
                 
                 tr1_min, tr1_max, tc1_min, tc1_max = temp_bbox1
                 tr2_min, tr2_max, tc2_min, tc2_max = temp_bbox2

                 gap_r_min = tr1_max + 1
                 gap_r_max = tr2_min - 1

                 if gap_r_min <= gap_r_max:
                     # Check if the gap area is entirely white
                     gap_area = input_grid[gap_r_min : gap_r_max + 1, overlap_c_min : overlap_c_max + 1]
                     if np.all(gap_area == 0):
                         # Fill the gap with azure (8)
                         output_grid[gap_r_min : gap_r_max + 1, overlap_c_min : overlap_c_max + 1] = 8

    return output_grid