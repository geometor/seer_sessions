```python
"""
This program transforms an input grid based on identifying and processing specific objects within it. 
The transformation logic depends on the types of objects found in the input grid.

General Workflow:
1. Identify all connected regions (objects) of non-background ('8') cells using 4-way connectivity.
2. Determine the transformation case based on the colors present in the identified objects:
   - Case A (Train 2 Pattern): If objects containing both colors '3' and '9' exist.
   - Case B (Train 1 Pattern): If Case A doesn't apply, but objects containing color '0' exist.
   - Default Case: If neither Case A nor B applies (return background grid).
3. Select the relevant object(s) based on the determined case:
   - Case A: Select all objects containing both '3' and '9'.
   - Case B: Select the largest object containing '0'.
4. Determine the bounding box for the single output object based on the selected object(s) and the case:
   - Case A: Calculate the bounding box enclosing the geometric centers of the selected objects (using rounding for coordinates). Note: This might not perfectly match train_2's output bbox, suggesting a more complex calculation might be needed.
   - Case B: Use the bounding box of the single selected object. Note: Train_1 output suggests potential shifting/resizing not captured here.
5. Create the output grid, initialized with the background color ('8').
6. Populate the determined output bounding box in the output grid based on the case:
   - Case A: Draw border with '3', fill interior with '9', then overlay '3's from input objects based on relative positions mapped between input object centers and the output box center.
   - Case B: Draw border with '7', then copy the content of the selected input object into the output box interior, mapping based on relative positions between the input object center and the output box center.
"""

import numpy as np
from collections import deque, namedtuple
import math

# Define structure for object properties
# Bbox is (min_row, min_col, max_row_inclusive, max_col_inclusive)
Object = namedtuple("Object", ["label", "coords", "colors", "bbox", "center", "size"])

def find_objects(grid: np.ndarray, background_color: int) -> list[Object]:
    """
    Identifies connected regions (objects) of non-background colors using BFS.

    Args:
        grid: The input numpy array.
        background_color: The integer value representing the background.

    Returns:
        A list of Object namedtuples.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    label_counter = 1

    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color and not visited[r, c]:
                # Start BFS for a new object
                q = deque([(r, c)])
                visited[r, c] = True
                current_coords = []
                current_colors = set()
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    current_coords.append((row, col))
                    current_colors.add(grid[row, col])
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Explore 4-way neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if (0 <= nr < height and 0 <= nc < width and
                                not visited[nr, nc] and
                                grid[nr, nc] != background_color):
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if current_coords:
                    coords_array = np.array(current_coords)
                    # Calculate geometric center (centroid)
                    center_r = np.mean(coords_array[:, 0])
                    center_c = np.mean(coords_array[:, 1])
                    
                    objects.append(Object(
                        label=label_counter,
                        coords=coords_array,
                        colors=current_colors,
                        bbox=(min_r, min_c, max_r, max_c),
                        center=(center_r, center_c),
                        size=len(current_coords)
                    ))
                    label_counter += 1
    return objects

def transform(input_grid_list: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on object identification and rule-based processing.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    height, width = input_grid.shape
    background_color = 8
    output_grid = np.full_like(input_grid, background_color)

    # 1. Find all non-background objects
    objects = find_objects(input_grid, background_color)
    if not objects:
        return output_grid.tolist()

    # 2. Determine transformation case and select objects
    selected_objects = []
    case = None
    
    # Check for Case A (Train 2 pattern: objects with {3, 9})
    case_a_candidates = [obj for obj in objects if {3, 9}.issubset(obj.colors)]
    if case_a_candidates:
        selected_objects = case_a_candidates
        case = 'A'
    else:
        # Check for Case B (Train 1 pattern: objects with '0')
        case_b_candidates = [obj for obj in objects if 0 in obj.colors]
        if case_b_candidates:
            # Select the largest object containing '0'
            selected_objects = [max(case_b_candidates, key=lambda obj: obj.size)]
            case = 'B'

    # If no relevant objects found for known cases
    if not selected_objects or case is None:
        return output_grid.tolist()

    # 3. Determine the output bounding box
    min_r_bbox, min_c_bbox, max_r_bbox, max_c_bbox = -1, -1, -1, -1

    if case == 'A':
        # Case A: Bbox from centers of multiple objects
        centers = [obj.center for obj in selected_objects]
        if not centers: return output_grid.tolist() # Should not happen if selected_objects is not empty
        
        center_rows = [r for r, c in centers]
        center_cols = [c for r, c in centers]
        
        # Calculate bbox by rounding min/max center coordinates
        # Note: This might not perfectly match the observed output bbox for train_2
        min_r_bbox = int(round(min(center_rows)))
        max_r_bbox = int(round(max(center_rows)))
        min_c_bbox = int(round(min(center_cols)))
        max_c_bbox = int(round(max(center_cols)))
        
    elif case == 'B':
        # Case B: Bbox from the single selected object
        # Note: Train_1 output suggests potential shifts/resizes not accounted for here.
        single_obj = selected_objects[0]
        min_r_bbox, min_c_bbox, max_r_bbox, max_c_bbox = single_obj.bbox

    # Ensure bbox coordinates are valid and within grid dimensions
    if min_r_bbox == -1: # Check if bbox was determined
         return output_grid.tolist()
         
    min_r_bbox = max(0, min_r_bbox)
    min_c_bbox = max(0, min_c_bbox)
    max_r_bbox = min(height - 1, max_r_bbox)
    max_c_bbox = min(width - 1, max_c_bbox)

    # Handle degenerate cases where bbox might be invalid
    if min_r_bbox > max_r_bbox or min_c_bbox > max_c_bbox:
        return output_grid.tolist()

    # 4. Calculate output box center (needed for relative positioning)
    out_center_r = (min_r_bbox + max_r_bbox) / 2.0
    out_center_c = (min_c_bbox + max_c_bbox) / 2.0

    # 5. Populate the output bounding box
    if case == 'A':
        border_color = 3
        fill_color = 9
        overlay_color = 3
        
        # Fill border and interior first
        for r in range(min_r_bbox, max_r_bbox + 1):
            for c in range(min_c_bbox, max_c_bbox + 1):
                is_border = (r == min_r_bbox or r == max_r_bbox or
                             c == min_c_bbox or c == max_c_bbox)
                output_grid[r, c] = border_color if is_border else fill_color

        # Overlay the 'overlay_color' from selected input objects
        for obj in selected_objects:
            obj_center_r, obj_center_c = obj.center
            for r_in, c_in in obj.coords:
                if input_grid[r_in, c_in] == overlay_color:
                    delta_r = r_in - obj_center_r
                    delta_c = c_in - obj_center_c
                    r_out = int(round(out_center_r + delta_r))
                    c_out = int(round(out_center_c + delta_c))

                    # Check if target is strictly *inside* the output bbox and within grid bounds
                    if (min_r_bbox < r_out < max_r_bbox and
                        min_c_bbox < c_out < max_c_bbox and
                        0 <= r_out < height and 0 <= c_out < width):
                         output_grid[r_out, c_out] = overlay_color

    elif case == 'B':
        border_color = 7
        single_obj = selected_objects[0]
        obj_center_r, obj_center_c = single_obj.center

        # Draw border
        for r in range(min_r_bbox, max_r_bbox + 1):
             for c in range(min_c_bbox, max_c_bbox + 1):
                 is_border = (r == min_r_bbox or r == max_r_bbox or
                              c == min_c_bbox or c == max_c_bbox)
                 if is_border:
                     output_grid[r,c] = border_color
                 # Leave interior as background for now, will be filled by copy

        # Copy content from input object to output interior based on relative center positions
        for r_in, c_in in single_obj.coords:
            input_color = input_grid[r_in, c_in]
            delta_r = r_in - obj_center_r
            delta_c = c_in - obj_center_c
            r_out = int(round(out_center_r + delta_r))
            c_out = int(round(out_center_c + delta_c))
            
            # Check if target is strictly *inside* the output bbox and within grid bounds
            if (min_r_bbox < r_out < max_r_bbox and
                min_c_bbox < c_out < max_c_bbox and
                0 <= r_out < height and 0 <= c_out < width):
                 output_grid[r_out, c_out] = input_color # Copy original color

    return output_grid.tolist()
```