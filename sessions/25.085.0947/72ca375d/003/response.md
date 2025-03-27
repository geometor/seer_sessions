```python
import numpy as np
from typing import List, Tuple, Dict, Any, Set

"""
Identifies all distinct non-white objects in the input grid using 8-connectivity.
Calculates properties for each object: area, bounding box (bbox), bbox area, and density (area / bbox_area).
Selects the object based on the following criteria, applied sequentially:
1. Maximum density.
2. Maximum area (among objects tied for maximum density).
3. Earliest top-left corner (minimum row, then minimum column) of the bbox (among objects tied for maximum density and maximum area).
Returns the subgrid corresponding to the bounding box of the selected object.
"""

def get_neighbors_8_conn(r: int, c: int, height: int, width: int) -> List[Tuple[int, int]]:
    """Gets the valid 8-connectivity neighbors (orthogonal and diagonal) of a cell."""
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def find_objects_8_conn(grid: np.ndarray) -> List[Dict[str, Any]]:
    """
    Finds all distinct contiguous objects (using 8-connectivity) of non-white color.

    Args:
        grid: The input numpy array representing the grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains 'color', 'pixels' (set of (r, c) tuples), 'area',
        'bbox' (min_r, max_r, min_c, max_c), 'bbox_area', and 'density'.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # Start BFS from a non-white pixel that hasn't been visited yet
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_pixels: Set[Tuple[int, int]] = set()
                q: List[Tuple[int, int]] = [(r, c)]
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c
                
                # Use a set to quickly check if a neighbor is already queued or processed for *this* object
                processed_in_this_obj: Set[Tuple[int, int]] = set([(r,c)]) 

                head = 0
                while head < len(q):
                    curr_r, curr_c = q[head]
                    head += 1
                    
                    obj_pixels.add((curr_r, curr_c))
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors
                    for nr, nc in get_neighbors_8_conn(curr_r, curr_c, height, width):
                        # Check if neighbor is same color, not globally visited, and not already processed for this object
                        if grid[nr, nc] == color and not visited[nr, nc] and (nr, nc) not in processed_in_this_obj:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            processed_in_this_obj.add((nr, nc))
                
                # Calculate properties for the found object
                area = len(obj_pixels)
                if area > 0: # Should always be true if we start BFS correctly
                    bbox = (min_r, max_r, min_c, max_c)
                    bbox_h = max_r - min_r + 1
                    bbox_w = max_c - min_c + 1
                    bbox_area = bbox_h * bbox_w
                    # Avoid division by zero, although bbox_area should be > 0 if area > 0
                    density = area / bbox_area if bbox_area > 0 else 0 

                    objects.append({
                        'color': color,
                        'pixels': obj_pixels,
                        'area': area,
                        'bbox': bbox,         # (min_r, max_r, min_c, max_c)
                        'bbox_area': bbox_area,
                        'density': density
                    })

    return objects


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    """
    
    # 1. Find all distinct non-white objects using 8-connectivity and calculate properties
    objects = find_objects_8_conn(input_grid)

    # Handle case where no non-white objects are found
    if not objects:
        # Return an empty grid or a default grid as appropriate.
        # Based on ARC tasks, this is unlikely for valid inputs, but good practice.
        # Returning a 1x1 white grid might be safer than an empty array.
        return np.zeros((1, 1), dtype=int) 

    # 2. Find the maximum density
    max_density = -1.0
    for obj in objects:
        if obj['density'] > max_density:
            max_density = obj['density']

    # 3. Filter objects to get candidates with maximum density
    # Use a small tolerance for floating point comparison
    density_candidates = [obj for obj in objects if abs(obj['density'] - max_density) < 1e-9]

    # 4. Apply tie-breaker 1: Maximum Area
    selected_object = None
    if len(density_candidates) == 1:
        selected_object = density_candidates[0]
    else:
        max_area = -1
        for obj in density_candidates:
            if obj['area'] > max_area:
                max_area = obj['area']
        
        area_candidates = [obj for obj in density_candidates if obj['area'] == max_area]

        # 5. Apply tie-breaker 2: Earliest Top-Left BBox Corner
        if len(area_candidates) == 1:
            selected_object = area_candidates[0]
        else:
            # Sort by min_row (bbox[0]), then min_col (bbox[2])
            area_candidates.sort(key=lambda o: (o['bbox'][0], o['bbox'][2]))
            selected_object = area_candidates[0] # Select the first one after sorting

    # Should have a selected object if the initial objects list was not empty
    if selected_object is None:
         # This case should ideally not be reached if input has objects
         return np.zeros((1, 1), dtype=int)

    # 6. Extract the output subgrid based on the selected object's bounding box
    min_r, max_r, min_c, max_c = selected_object['bbox']
    output_grid = input_grid[min_r:max_r+1, min_c:max_c+1]

    return output_grid
```