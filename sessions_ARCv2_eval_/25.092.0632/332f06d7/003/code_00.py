import numpy as np
from collections import deque
from typing import Set, Tuple, Optional, List, FrozenSet

"""
Transformation rule based on object shapes and colors:

1.  Identify the single contiguous white (0) object (W) and the single 
    contiguous red (2) object (R) using 8-directional connectivity. 
    Determine their shapes relative to their top-left corners (shapeW, shapeR) 
    and their absolute coordinates (W_coords, R_coords).
2.  Identify all blue (1) pixels in the input grid (B_pixels).
3.  Initialize the output grid as a copy of the input grid.
4.  **Mandatory Change:** Change all pixels at W_coords to blue (1) in the output grid.
5.  **Conditional Changes:**
    a. Search within the original blue pixels (B_pixels) for a contiguous 
       sub-region that exactly matches shapeW. Let the coordinates of the first 
       such sub-region found be `TargetB_W_coords`.
    b. **Case 1: shapeW == shapeR**
        i. If `TargetB_W_coords` exists (a blue sub-region matching W was found):
           - Change the pixels at `TargetB_W_coords` to white (0) in the output grid.
           - Leave the red object R unchanged.
        ii. If `TargetB_W_coords` does not exist:
           - Change the pixels at `R_coords` (the red object) to white (0) in the output grid.
    c. **Case 2: shapeW != shapeR**
        i. Leave the red object R unchanged.
        ii. If `TargetB_W_coords` exists:
            - Change the pixels at `TargetB_W_coords` to white (0) in the output grid.
        iii. If `TargetB_W_coords` does not exist:
            - Search within the original blue pixels (B_pixels) for a contiguous 
              sub-region that exactly matches shapeR. Let the first found be 
              `TargetB_R_coords`.
            - If `TargetB_R_coords` exists:
                - Change the pixels at `TargetB_R_coords` to white (0) in the output grid.
            - (Else: If neither matching sub-region is found, no further blue pixels change).
6. Return the modified output grid.
"""

def find_objects(grid: np.ndarray, color: int, connectivity: int = 8) -> List[Set[Tuple[int, int]]]:
    """
    Finds all contiguous objects of a specific color in the grid using BFS.

    Args:
        grid (np.ndarray): The input grid.
        color (int): The color of the objects to find.
        connectivity (int): 4 or 8 for neighbor checking.

    Returns:
        list: A list of sets, where each set contains the (row, col) tuples
              of pixels belonging to a single contiguous object.
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
                obj_coords.add((r, c))

                while q:
                    row, col = q.popleft()
                    for dr, dc in deltas:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            obj_coords.add((nr, nc))
                
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def get_object_shape(obj_coords: Set[Tuple[int, int]]) -> FrozenSet[Tuple[int, int]]:
    """
    Calculates a canonical shape representation for an object.

    Args:
        obj_coords (set): A set of (row, col) tuples for the object's pixels.

    Returns:
        frozenset: A frozenset of relative (dr, dc) coordinates representing the shape,
                   normalized to the top-left corner (0, 0). Returns an empty
                   frozenset if obj_coords is empty.
    """
    if not obj_coords:
        return frozenset()
    
    min_r = min(r for r, c in obj_coords)
    min_c = min(c for r, c in obj_coords)
    
    shape = frozenset((r - min_r, c - min_c) for r, c in obj_coords)
    return shape

def find_subregion_with_shape(grid: np.ndarray, 
                               target_shape: FrozenSet[Tuple[int, int]], 
                               color_to_search: int) -> Optional[Set[Tuple[int, int]]]:
    """
    Searches the grid for the first contiguous sub-region of a specific color 
    that matches the target shape.

    Args:
        grid (np.ndarray): The grid to search within (should be the original input).
        target_shape (frozenset): The relative coordinates defining the shape.
        color_to_search (int): The color of pixels that can form the sub-region.

    Returns:
        Optional[Set[Tuple[int, int]]]: The absolute coordinates of the first 
                                         matching sub-region found, or None.
    """
    if not target_shape:
        return None
        
    rows, cols = grid.shape
    
    # Iterate through all possible top-left anchor points in the grid
    for r_anchor in range(rows):
        for c_anchor in range(cols):
            # Check if the anchor pixel itself has the right color
            if grid[r_anchor, c_anchor] == color_to_search:
                match = True
                current_subregion_coords = set()
                
                # Check if all pixels defined by the shape relative to the anchor exist and have the correct color
                for dr, dc in target_shape:
                    nr, nc = r_anchor + dr, c_anchor + dc
                    
                    # Check bounds and color
                    if not (0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == color_to_search):
                        match = False
                        break # This anchor point doesn't work for this shape
                    current_subregion_coords.add((nr, nc))
                
                # If all pixels of the shape matched
                if match:
                    # Verify the size matches (ensures no extra pixels accidentally included if shape has holes)
                    if len(current_subregion_coords) == len(target_shape):
                         return current_subregion_coords # Found the first match

    return None # No matching sub-region found

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rules based on object shapes and colors.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify white (W) and red (R) objects
    white_objects = find_objects(input_grid, 0, connectivity=8)
    red_objects = find_objects(input_grid, 2, connectivity=8)

    # Assume exactly one white and one red object based on examples
    if not white_objects or not red_objects:
        # If assumptions fail, return the unchanged grid or handle error
        return output_grid 
        
    w_coords = white_objects[0]
    r_coords = red_objects[0]

    # 2. Determine shapes
    shapeW = get_object_shape(w_coords)
    shapeR = get_object_shape(r_coords)

    # (Step 3 is implicit: B_pixels are checked within find_subregion_with_shape)

    # 4. Mandatory Change: White becomes Blue
    for r, c in w_coords:
        if 0 <= r < rows and 0 <= c < cols: # Bounds check just in case
             output_grid[r, c] = 1

    # 5. Conditional Changes
    
    # 5a. Search for blue sub-region matching white shape in the *original* grid
    targetB_W_coords = find_subregion_with_shape(input_grid, shapeW, 1)

    # 5b. Case 1: shapeW == shapeR
    if shapeW == shapeR:
        if targetB_W_coords is not None:
            # Change the found blue sub-region to white
            for r, c in targetB_W_coords:
                 if 0 <= r < rows and 0 <= c < cols:
                    output_grid[r, c] = 0
            # Leave red object unchanged
        else:
            # Change the red object to white
            for r, c in r_coords:
                if 0 <= r < rows and 0 <= c < cols:
                    output_grid[r, c] = 0
    
    # 5c. Case 2: shapeW != shapeR
    else:
        # Leave red object unchanged
        if targetB_W_coords is not None:
            # Change the found blue sub-region (matching white) to white
            for r, c in targetB_W_coords:
                if 0 <= r < rows and 0 <= c < cols:
                    output_grid[r, c] = 0
        else:
            # Search for blue sub-region matching red shape in the *original* grid
            targetB_R_coords = find_subregion_with_shape(input_grid, shapeR, 1)
            if targetB_R_coords is not None:
                # Change the found blue sub-region (matching red) to white
                for r, c in targetB_R_coords:
                    if 0 <= r < rows and 0 <= c < cols:
                        output_grid[r, c] = 0
            # Else: No matching blue sub-regions found for either shape, no further changes.

    # 6. Return the result
    return output_grid