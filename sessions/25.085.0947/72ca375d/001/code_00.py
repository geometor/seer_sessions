import numpy as np
from typing import List, Tuple, Dict, Any

"""
Identifies all distinct non-white objects in the input grid.
Calculates the density (area / bounding_box_area) for each object.
Selects the object with the highest density.
If there's a tie in density, selects the object with the largest area among the tied objects.
Returns the subgrid corresponding to the bounding box of the selected object.
"""

def get_neighbors(r: int, c: int, height: int, width: int) -> List[Tuple[int, int]]:
    """Gets the valid orthogonal neighbors of a cell."""
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 4-connectivity
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def find_objects(grid: np.ndarray) -> List[Dict[str, Any]]:
    """
    Finds all distinct contiguous objects of non-white color in the grid.

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
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = set()
                q = [(r, c)]
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    curr_r, curr_c = q.pop(0)
                    obj_pixels.add((curr_r, curr_c))
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    for nr, nc in get_neighbors(curr_r, curr_c, height, width):
                        if grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Calculate properties
                area = len(obj_pixels)
                bbox = (min_r, max_r, min_c, max_c)
                bbox_h = max_r - min_r + 1
                bbox_w = max_c - min_c + 1
                bbox_area = bbox_h * bbox_w
                density = area / bbox_area if bbox_area > 0 else 0

                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'area': area,
                    'bbox': bbox,
                    'bbox_area': bbox_area,
                    'density': density
                })

    return objects

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    """
    # 1. Identify Objects and calculate properties
    objects = find_objects(input_grid)

    if not objects:
        # Handle case with no objects (return empty grid or input?)
        # Based on examples, this shouldn't happen, but good practice.
        return np.array([[]], dtype=int) 

    # 2. Find Maximum Density
    max_density = -1.0
    for obj in objects:
        if obj['density'] > max_density:
            max_density = obj['density']

    # 3. Filter by Maximum Density
    candidates = [obj for obj in objects if obj['density'] == max_density]

    # 4. Apply Tie-Breaker (Largest Area)
    selected_object = None
    if len(candidates) == 1:
        selected_object = candidates[0]
    else:
        max_area = -1
        for obj in candidates:
            if obj['area'] > max_area:
                max_area = obj['area']
                selected_object = obj
        # Note: If there's still a tie in area after density tie,
        # this selects the last one encountered with max_area. 
        # The problem description doesn't specify further tie-breaking.

    if selected_object is None:
         # Should not happen if objects list was not empty
         return np.array([[]], dtype=int) 

    # 5. Extract Output Subgrid
    min_r, max_r, min_c, max_c = selected_object['bbox']
    output_grid = input_grid[min_r:max_r+1, min_c:max_c+1]

    return output_grid