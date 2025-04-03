import numpy as np
from collections import deque
from typing import Set, Tuple, Optional, List, FrozenSet, Dict

"""
Transforms grid by swapping colors based on object shapes. A white object 
always becomes blue. Either the red object or a blue object becomes white 
based on shape comparison and existence of matching blue objects.

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the single contiguous white object (W). Store its coordinates 
    (`W_coords`) and calculate its canonical shape (`shapeW`).
3.  Identify the single contiguous red object (R). Store its coordinates 
    (`R_coords`) and calculate its canonical shape (`shapeR`).
4.  Identify all contiguous blue objects ({B}). For each blue object `Bi`, store 
    its coordinates (`Bi_coords`), calculate its canonical shape (`shapeBi`), and
    determine its top-left anchor point (`Bi_anchor`).
5.  **Mandatory Change:** Change all pixels at `W_coords` in the output grid to 
    blue (1).
6.  Find all blue objects `Bk` from {B} such that `shapeBk == shapeW`. Let this 
    collection be `MatchingW_BlueObjects`.
7.  Find all blue objects `Bj` from {B} such that `shapeBj == shapeR`. Let this 
    collection be `MatchingR_BlueObjects`.
8.  **Conditional Change (Object to become White):**
    a.  **IF `shapeW == shapeR`:**
        i.  IF `MatchingW_BlueObjects` is **empty**:
            Change all pixels at `R_coords` in the output grid to white (0).
        ii. ELSE (`MatchingW_BlueObjects` is **not empty**):
            Select one target object `Bt` from `MatchingW_BlueObjects` (e.g., the 
            one with the largest top-left anchor: max row, then max col).
            Change all pixels at `Bt_coords` in the output grid to white (0).
            *(Note: This step correctly handles Ex2, Ex3, but incorrectly handles 
            Ex1, Ex4 based on expected outputs).*
    b.  **ELSE (`shapeW != shapeR`):**
        i.  IF `MatchingW_BlueObjects` is **not empty**:
            Select one target object `Bt` from `MatchingW_BlueObjects` (using the 
            same selection rule).
            Change all pixels at `Bt_coords` in the output grid to white (0).
        ii. ELSE (`MatchingW_BlueObjects` is **empty**):
            IF `MatchingR_BlueObjects` is **not empty**:
                Select one target object `Bt` from `MatchingR_BlueObjects` (using 
                the same selection rule).
                Change all pixels at `Bt_coords` in the output grid to white (0).
            ELSE:
                No object changes to white (only W changed to blue).
9.  Return the modified output grid.
"""

# --- Helper Functions ---

def find_objects(grid: np.ndarray, color: int, connectivity: int = 8) -> List[Dict]:
    """
    Finds all contiguous objects of a specific color in the grid using BFS.
    Returns a list of dictionaries, each containing 'coords' and 'anchor'.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    if connectivity == 8:
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    else: # Default to 4-connectivity
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c  # Initialize anchor

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)

                    for dr, dc in deltas:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if obj_coords:
                    # Recalculate anchor accurately after finding all coords
                    current_min_r = min(coord[0] for coord in obj_coords)
                    current_min_c = min(coord[1] for coord in obj_coords)
                    objects.append({
                        'coords': obj_coords,
                        'anchor': (current_min_r, current_min_c)
                    })
    return objects

def get_object_shape(obj_coords: Set[Tuple[int, int]]) -> FrozenSet[Tuple[int, int]]:
    """
    Calculates a canonical shape representation for an object.
    """
    if not obj_coords:
        return frozenset()
    
    min_r = min(r for r, c in obj_coords)
    min_c = min(c for r, c in obj_coords)
    
    shape = frozenset((r - min_r, c - min_c) for r, c in obj_coords)
    return shape

def select_target_blue_object(candidate_objects: List[Dict]) -> Optional[Dict]:
    """
    Selects one blue object from the candidates based on the largest anchor.
    Largest anchor means: max row, then max column.
    """
    if not candidate_objects:
        return None
    
    # Sort by anchor: primarily by row (descending), secondarily by col (descending)
    # Since max() finds the first maximum in case of ties in the primary key, 
    # we sort first by col (ascending), then by row (ascending) and take the last element.
    # Alternatively, use a custom key with max().
    
    # Using max with a custom key (row, col)
    selected_object = max(candidate_objects, key=lambda obj: obj['anchor'])
    
    return selected_object

# --- Main Transformation Function ---

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rules based on object shapes and colors.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify white (W) object
    white_objects_data = find_objects(input_grid, 0, connectivity=8)
    if not white_objects_data: return output_grid # Should not happen per task desc
    w_data = white_objects_data[0]
    w_coords = w_data['coords']
    shapeW = get_object_shape(w_coords)

    # 2. Identify red (R) object
    red_objects_data = find_objects(input_grid, 2, connectivity=8)
    if not red_objects_data: return output_grid # Should not happen per task desc
    r_data = red_objects_data[0]
    r_coords = r_data['coords']
    shapeR = get_object_shape(r_coords)

    # 3. Identify all blue (B) objects and calculate shapes/anchors
    blue_objects_data = find_objects(input_grid, 1, connectivity=8)
    for b_obj in blue_objects_data:
        b_obj['shape'] = get_object_shape(b_obj['coords'])

    # 4. Mandatory Change: White becomes Blue
    for r, c in w_coords:
        if 0 <= r < rows and 0 <= c < cols:
             output_grid[r, c] = 1

    # 5. Filter blue objects matching W's shape
    matchingW_blue_objects = [b for b in blue_objects_data if b['shape'] == shapeW]

    # 6. Filter blue objects matching R's shape
    matchingR_blue_objects = [b for b in blue_objects_data if b['shape'] == shapeR]
    
    # 7. Conditional Change (Object to become White)
    target_coords_to_make_white = None

    # 7a. Case: shapeW == shapeR
    if shapeW == shapeR:
        if not matchingW_blue_objects:
            # 7a.i: No blue object matches W/R shape -> R becomes White
            target_coords_to_make_white = r_coords
        else:
            # 7a.ii: Blue object(s) match W/R shape -> Select one B and make it White
            # (Note: This branch correctly handles Ex2, Ex3, but fails Ex1, Ex4)
            selected_blue_obj = select_target_blue_object(matchingW_blue_objects)
            if selected_blue_obj:
                target_coords_to_make_white = selected_blue_obj['coords']
            # If selection fails (shouldn't if list is not empty), R remains unchanged implicitly
            
    # 7b. Case: shapeW != shapeR
    else:
        if matchingW_blue_objects:
            # 7b.i: Blue object(s) match W shape -> Select one B and make it White
            selected_blue_obj = select_target_blue_object(matchingW_blue_objects)
            if selected_blue_obj:
                target_coords_to_make_white = selected_blue_obj['coords']
        else:
            # 7b.ii: No blue object matches W shape. Check for match with R shape.
            if matchingR_blue_objects:
                selected_blue_obj = select_target_blue_object(matchingR_blue_objects)
                if selected_blue_obj:
                    target_coords_to_make_white = selected_blue_obj['coords']
            # Else: No blue object matches W or R shape -> No further changes

    # Apply the change to white if a target was determined
    if target_coords_to_make_white:
        for r, c in target_coords_to_make_white:
             if 0 <= r < rows and 0 <= c < cols:
                 # Ensure we don't overwrite a pixel that just turned blue from white, 
                 # although this shouldn't happen if objects are distinct.
                 # Check original color? No, just apply based on determined target coords.
                 output_grid[r, c] = 0

    # 8. Return the result
    return output_grid