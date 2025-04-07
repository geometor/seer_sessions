"""
Identify all distinct objects (connected components of the same non-zero digit) in the input grid using orthogonal connectivity.
For each object, calculate its mass (cell count), bounding box (min/max row/col), bounding box area, and density (mass/area).
Filter out objects with density 1.0 AND mass 1, unless this would remove all objects.
From the filtered list, find the object(s) with the maximum density.
If there's a tie in density, select the object(s) among the tied ones with the largest bounding box area.
If there's still a tie (same max density and same max area), select the object(s) among the tied ones with the largest mass.
If a tie still persists, select the first object found among the final tied set.
Return the subgrid from the input corresponding to the bounding box of the selected object.
"""

import collections
import numpy as np # Use numpy for easier slicing

def get_bounding_box(coords):
    """Calculates the bounding box and its area for a set of coordinates."""
    if not coords:
        return None, 0
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    area = height * width
    # Returns (min_row, max_row, min_col, max_col), area
    return (min_r, max_r, min_c, max_c), area

def find_objects(grid: list[list[int]]) -> list[dict]:
    """Finds all connected components of non-zero cells in the grid."""
    grid_np = np.array(grid)
    rows, cols = grid_np.shape
    if rows == 0 or cols == 0:
        return []
        
    visited = set()
    objects = [] # List to store dicts: {'id': id, 'color': color, 'coords': set_of_coords}
    object_id_counter = 0

    for r in range(rows):
        for c in range(cols):
            if grid_np[r, c] != 0 and (r, c) not in visited:
                color = grid_np[r, c]
                current_object_coords = set()
                queue = collections.deque([(r, c)])
                visited.add((r, c))
                
                while queue:
                    row, col = queue.popleft()
                    current_object_coords.add((row, col))
                    
                    # Check orthogonal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and \
                           grid_np[nr, nc] == color:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
                
                if current_object_coords:
                     objects.append({
                         'id': object_id_counter,
                         'color': int(color), # Ensure color is int
                         'coords': current_object_coords
                     })
                     object_id_counter += 1
    return objects

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on density, area, and mass tie-breaking.
    """
    input_np = np.array(input_grid) # Convert to numpy array for easier slicing

    # 1. Find all distinct objects
    found_objects = find_objects(input_grid)

    # Handle case where no objects are found
    if not found_objects:
        return []

    # 2. Calculate properties for each object
    object_details = []
    for obj in found_objects:
        coords = obj['coords']
        bbox, area = get_bounding_box(coords)
        if bbox is None: # Should not happen if found_objects is not empty
            continue

        mass = len(coords)
        density = mass / area if area > 0 else 0
        
        object_details.append({
            'id': obj['id'],
            'color': obj['color'],
            'coords': coords,
            'mass': mass,
            'bbox': bbox,
            'area': area,
            'density': density
        })

    # Handle case where no valid object details were generated
    if not object_details:
         return []

    # 3. Filter out single-cell objects with density 1.0
    filtered_objects = [
        obj for obj in object_details
        if not (obj['density'] == 1.0 and obj['mass'] == 1)
    ]
    # Use the filtered list unless it's empty, otherwise revert to original
    candidate_objects = filtered_objects if filtered_objects else object_details

    # 4. Find max density among candidates
    if not candidate_objects: # Should not happen based on previous checks, but safety first
        return []
    max_density = -1.0
    for obj in candidate_objects:
        if obj['density'] > max_density:
            max_density = obj['density']

    # 5. Select objects with max density
    primary_candidates = [obj for obj in candidate_objects if obj['density'] == max_density]

    # 6. Tie-break by max area (if necessary)
    if len(primary_candidates) > 1:
        max_area = -1
        for obj in primary_candidates:
            if obj['area'] > max_area:
                max_area = obj['area']
        secondary_candidates = [obj for obj in primary_candidates if obj['area'] == max_area]
    else:
        secondary_candidates = primary_candidates

    # 7. Tie-break by max mass (if necessary)
    if len(secondary_candidates) > 1:
        max_mass = -1
        for obj in secondary_candidates:
            if obj['mass'] > max_mass:
                max_mass = obj['mass']
        tertiary_candidates = [obj for obj in secondary_candidates if obj['mass'] == max_mass]
    else:
        tertiary_candidates = secondary_candidates

    # 8. Select the final object (first if still tied)
    if not tertiary_candidates:
        # This case should ideally not be reached if input processing is correct
        # But as a fallback, maybe return the first object overall? Or empty? Let's return empty.
        return []
        
    target_object = tertiary_candidates[0]

    # 9. Extract the bounding box subgrid
    min_r, max_r, min_c, max_c = target_object['bbox']
    # Use numpy slicing: [row_start:row_end+1, col_start:col_end+1]
    output_np = input_np[min_r : max_r + 1, min_c : max_c + 1]

    # Convert back to list of lists for the expected output format
    output_grid = output_np.tolist()

    return output_grid