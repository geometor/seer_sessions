import numpy as np
from collections import deque

"""
Transforms an input grid by identifying four specific non-'1' objects outside the 
largest '1'-boundary, extracting their 3x3 shape representations, and arranging 
these shapes into the four quadrants of a 7x7 output grid based on their 
relative spatial positions in the input.

The transformation steps are:
1. Convert the input list of lists into a NumPy array.
2. Find all connected components (objects) of non-zero cells in the input grid.
3. Identify the largest object composed of the digit '1'. If no '1' object exists, 
   proceed assuming no boundary filtering is needed.
4. Filter out the '1' object(s) and any objects completely enclosed within the 
   bounding box of the largest '1' object.
5. Identify the four remaining target objects. It's assumed there will be exactly four.
6. For each target object:
    a. Calculate its geometric center.
    b. Extract its shape into a 3x3 grid, maintaining its top-left alignment 
       relative to its bounding box.
7. Calculate the overall geometric center of the centers of the four target objects.
8. Determine the relative quadrant (Top-Left, Top-Right, Bottom-Left, Bottom-Right) 
   for each target object based on its center's position relative to the overall center.
9. Initialize a 7x7 output grid filled with zeros.
10. Place the 3x3 shape grid of each target object into the corresponding quadrant 
    of the output grid:
    - Top-Left object -> Output[0:3, 0:3]
    - Top-Right object -> Output[0:3, 4:7]
    - Bottom-Left object -> Output[4:7, 0:3]
    - Bottom-Right object -> Output[4:7, 4:7]
11. Convert the resulting NumPy array back to a list of lists and return it.
"""

def _find_objects(grid: np.ndarray) -> list[dict]:
    """Finds all connected components of non-zero cells."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                
                current_object_coords = [] # Store coords for center calculation

                while q:
                    row, col = q.popleft()
                    coords.add((row, col))
                    current_object_coords.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 4 neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                bbox = (min_r, min_c, max_r, max_c)
                # Calculate center
                center_r = sum(r for r, c in current_object_coords) / len(current_object_coords)
                center_c = sum(c for r, c in current_object_coords) / len(current_object_coords)
                center = (center_r, center_c)

                objects.append({'color': color, 'coords': coords, 'bbox': bbox, 'center': center, 'size': len(coords)})
    return objects

def _get_bounding_box(coords: set) -> tuple[int, int, int, int]:
    """Calculates the bounding box of a set of coordinates."""
    if not coords:
        return (0, 0, 0, 0)
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return (min_r, min_c, max_r, max_c)

def _is_inside(inner_bbox: tuple[int, int, int, int], outer_bbox: tuple[int, int, int, int]) -> bool:
    """Checks if inner_bbox is strictly inside outer_bbox."""
    inner_min_r, inner_min_c, inner_max_r, inner_max_c = inner_bbox
    outer_min_r, outer_min_c, outer_max_r, outer_max_c = outer_bbox
    return (inner_min_r >= outer_min_r and
            inner_min_c >= outer_min_c and
            inner_max_r <= outer_max_r and
            inner_max_c <= outer_max_c)
            
def _extract_shape_3x3(grid: np.ndarray, obj: dict) -> np.ndarray:
    """Extracts the object's shape into a 3x3 grid relative to its bbox top-left."""
    subgrid = np.zeros((3, 3), dtype=int)
    min_r, min_c, _, _ = obj['bbox']
    color = obj['color']
    for r, c in obj['coords']:
        rel_r = r - min_r
        rel_c = c - min_c
        if 0 <= rel_r < 3 and 0 <= rel_c < 3:
            subgrid[rel_r, rel_c] = color # Use object's color
    return subgrid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the perceived rules.
    """
    grid = np.array(input_grid, dtype=int)
    
    # 1. Find all objects
    all_objects = _find_objects(grid)

    # 2. Find the largest '1' object (boundary)
    one_objects = [obj for obj in all_objects if obj['color'] == 1]
    largest_one_object = None
    if one_objects:
        largest_one_object = max(one_objects, key=lambda obj: obj['size'])
    
    # 3. Filter objects
    target_objects = []
    if largest_one_object:
        one_bbox = largest_one_object['bbox']
        for obj in all_objects:
            if obj['color'] != 1 and not _is_inside(obj['bbox'], one_bbox):
                 target_objects.append(obj)
    else: # No '1' boundary found, keep all non-'1' objects
         for obj in all_objects:
            if obj['color'] != 1:
                 target_objects.append(obj)

    # Expecting exactly 4 target objects
    if len(target_objects) != 4:
        # Handle error or unexpected case. For now, proceed assuming 4.
        # Maybe raise an error or return a default grid?
        # Let's try to proceed if possible, might fail later
         pass 
         # print(f"Warning: Expected 4 target objects, found {len(target_objects)}")

    # 4. Calculate overall center
    if not target_objects:
         # Handle case with no target objects
         return [[0]*7 for _ in range(7)] # Return empty 7x7

    avg_center_r = sum(obj['center'][0] for obj in target_objects) / len(target_objects)
    avg_center_c = sum(obj['center'][1] for obj in target_objects) / len(target_objects)

    # 5. Determine quadrants and extract 3x3 shapes
    object_shapes = {} # Store shapes keyed by quadrant: 'TL', 'TR', 'BL', 'BR'
    
    assigned_quadrants = set()

    for obj in target_objects:
        obj_r, obj_c = obj['center']
        shape_3x3 = _extract_shape_3x3(grid, obj)
        
        quadrant = ""
        if obj_r < avg_center_r and obj_c < avg_center_c:
            quadrant = 'TL'
        elif obj_r < avg_center_r and obj_c >= avg_center_c:
            quadrant = 'TR'
        elif obj_r >= avg_center_r and obj_c < avg_center_c:
             quadrant = 'BL'
        else: # obj_r >= avg_center_r and obj_c >= avg_center_c
             quadrant = 'BR'

        # Handle potential quadrant conflicts if centers are very close
        original_quadrant = quadrant
        counter = 0
        while quadrant in assigned_quadrants and counter < 4:
            # Simple conflict resolution: try next clockwise quadrant
            if quadrant == 'TL': quadrant = 'TR'
            elif quadrant == 'TR': quadrant = 'BR'
            elif quadrant == 'BR': quadrant = 'BL'
            elif quadrant == 'BL': quadrant = 'TL'
            counter += 1
        
        if quadrant in assigned_quadrants:
             # If still conflicting after rotating, something is wrong or objects are too clustered
             # For now, overwrite - the last object processed for a quadrant wins
             print(f"Warning: Quadrant conflict for {original_quadrant}, overwriting.")


        object_shapes[quadrant] = shape_3x3
        assigned_quadrants.add(quadrant)


    # 6. Construct the output grid
    output_grid = np.zeros((7, 7), dtype=int)
    
    if 'TL' in object_shapes:
        output_grid[0:3, 0:3] = object_shapes['TL']
    if 'TR' in object_shapes:
        output_grid[0:3, 4:7] = object_shapes['TR']
    if 'BL' in object_shapes:
        output_grid[4:7, 0:3] = object_shapes['BL']
    if 'BR' in object_shapes:
        output_grid[4:7, 4:7] = object_shapes['BR']

    # 7. Convert back to list of lists and return
    return output_grid.tolist()