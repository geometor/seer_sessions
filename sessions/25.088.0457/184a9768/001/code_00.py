import numpy as np
from collections import deque
import math

"""
Transformation Rule Description:

1.  Identify different types of objects in the input grid:
    *   Container Objects: Non-white, non-gray objects that enclose one or more regions of white pixels (pixels with value 0).
    *   Filler Objects: Non-white, non-gray objects that are *not* containers.
    *   Marker Objects: Gray pixels (pixels with value 5).
    *   Internal White Regions: Contiguous areas of white pixels completely surrounded by a single container object (i.e., they do not touch the grid border or any other non-white object).
    *   Background: White pixels (value 0).

2.  For each Internal White Region:
    a.  Find the closest Marker Object (gray pixel) to the region. Closeness is defined by the minimum Euclidean distance between any pixel of the region and any pixel of the marker object (typically a single pixel).
    b.  Find the closest Filler Object to that specific Marker Object. Closeness is defined similarly by minimum Euclidean distance.
    c.  Determine the color of this closest Filler Object.

3.  Construct the Output Grid:
    a.  Start with a grid of the same dimensions as the input, filled entirely with the background color (white, 0).
    b.  Copy the original Container Objects (pixels) onto the output grid.
    c.  For each Internal White Region identified in step 1, fill that region in the output grid with the corresponding Filler Object color determined in step 2c.
    d.  Original Filler Objects and Marker Objects are *not* copied to the output grid, unless their locations are overwritten by the filled internal regions.
"""

def find_objects(grid, condition_func):
    """Finds all contiguous objects satisfying a condition function."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if condition_func(grid[r, c]) and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_coords.add((r, c))
                color = grid[r,c] # Store color for consistency check if needed

                while q:
                    row, col = q.popleft()
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and \
                           condition_func(grid[nr, nc]) and \
                           grid[nr,nc] == color: # Ensure same color within object
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            obj_coords.add((nr, nc))
                objects.append({'coords': obj_coords, 'color': color})
    return objects

def get_neighbors(coords, grid_shape):
    """Gets all unique valid neighbor coordinates for a set of coordinates."""
    height, width = grid_shape
    neighbors = set()
    for r, c in coords:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
             nr, nc = r + dr, c + dc
             if 0 <= nr < height and 0 <= nc < width:
                 neighbors.add((nr, nc))
    # Remove the object's own coordinates
    neighbors -= coords
    return neighbors

def touches_border(coords, grid_shape):
    """Check if any coordinate in the set touches the grid border."""
    height, width = grid_shape
    for r, c in coords:
        if r == 0 or c == 0 or r == height - 1 or c == width - 1:
            return True
    return False

def min_euclidean_distance(coords1, coords2):
    """Calculates the minimum Euclidean distance between two sets of coordinates."""
    min_dist_sq = float('inf')
    if not coords1 or not coords2:
         return float('inf') # Should not happen if objects exist

    # Convert sets to lists for indexing if needed, though iterating works
    list1 = list(coords1)
    list2 = list(coords2)

    # Optimization: if sets are large, consider spatial indexing or other methods.
    # For ARC constraints (max 30x30), brute force is feasible.
    for r1, c1 in list1:
        for r2, c2 in list2:
            dist_sq = (r1 - r2)**2 + (c1 - c2)**2
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq

    return math.sqrt(min_dist_sq) if min_dist_sq != float('inf') else float('inf')


def transform(input_grid_list):
    """
    Transforms the input grid based on the rules derived from examples.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid) # Start with white background

    # 1. Find all relevant objects/regions
    markers = find_objects(input_grid, lambda x: x == 5) # Gray markers
    potential_containers_fillers = find_objects(input_grid, lambda x: x != 0 and x != 5) # Non-white, non-gray
    white_regions = find_objects(input_grid, lambda x: x == 0) # White regions

    marker_coords = [m['coords'] for m in markers] # List of sets of coords
    all_marker_pixels = set().union(*marker_coords) # Flattened set of all marker pixels


    # 2. Identify Containers, Fillers, and Internal White Regions
    containers = []
    fillers = []
    internal_regions_map = {} # Map: frozenset(region_coords) -> {'container_idx': int, 'fill_color': None}

    potential_map = {frozenset(obj['coords']): obj for obj in potential_containers_fillers}
    non_white_pixels = np.argwhere(input_grid != 0)
    non_white_coords = set(map(tuple, non_white_pixels))


    internal_candidate_regions = []
    for region in white_regions:
        if not touches_border(region['coords'], (height, width)):
            internal_candidate_regions.append(region)

    container_indices = {} # Map object coords (frozenset) to its index in `containers` list

    # Assign internal regions to containers and identify containers
    assigned_regions = set()
    for i, p_obj in enumerate(potential_containers_fillers):
        p_coords_fs = frozenset(p_obj['coords'])
        is_container = False
        for region in internal_candidate_regions:
            region_coords_fs = frozenset(region['coords'])
            if region_coords_fs in assigned_regions:
                continue # Already assigned

            neighbors = get_neighbors(region['coords'], (height, width))
            adjacent_non_white_coords = neighbors.intersection(non_white_coords)

            # Check if *all* adjacent non-white pixels belong *only* to this potential container
            if adjacent_non_white_coords and adjacent_non_white_coords.issubset(p_coords_fs):
                 is_container = True
                 if p_coords_fs not in container_indices:
                     container_indices[p_coords_fs] = len(containers)
                     containers.append(p_obj) # Add to containers list

                 container_idx = container_indices[p_coords_fs]
                 internal_regions_map[region_coords_fs] = {'container_idx': container_idx, 'fill_color': None}
                 assigned_regions.add(region_coords_fs) # Mark as assigned

        # If an object wasn't identified as a container after checking all regions, it's a filler
    # Correct filler identification: it's any potential object NOT in containers list
    container_coord_sets = {frozenset(c['coords']) for c in containers}
    fillers = [p_obj for p_obj in potential_containers_fillers if frozenset(p_obj['coords']) not in container_coord_sets]


    # 3. Determine fill color for each internal region
    for region_coords_fs, region_data in internal_regions_map.items():
        region_coords = set(region_coords_fs) # Unfreeze for distance calc if needed

        # a. Find closest marker to the region
        closest_marker_idx = -1
        min_dist_to_marker = float('inf')
        for idx, m_coords in enumerate(marker_coords):
            dist = min_euclidean_distance(region_coords, m_coords)
            if dist < min_dist_to_marker:
                min_dist_to_marker = dist
                closest_marker_idx = idx

        if closest_marker_idx == -1:
            # print(f"Warning: No marker found for region {region_coords_fs}")
            continue # Skip if no marker found

        closest_marker_coords = marker_coords[closest_marker_idx]

        # b. Find closest filler to that marker
        closest_filler_idx = -1
        min_dist_to_filler = float('inf')
        for idx, filler in enumerate(fillers):
            dist = min_euclidean_distance(closest_marker_coords, filler['coords'])
            if dist < min_dist_to_filler:
                min_dist_to_filler = dist
                closest_filler_idx = idx

        if closest_filler_idx == -1:
            # print(f"Warning: No filler found for marker near region {region_coords_fs}")
            continue # Skip if no filler found

        # c. Get filler color and store it
        fill_color = fillers[closest_filler_idx]['color']
        region_data['fill_color'] = fill_color


    # 4. Construct the output grid
    # a. Copy containers
    for container in containers:
        for r, c in container['coords']:
             # Check bounds just in case, though coords should be valid
             if 0 <= r < height and 0 <= c < width:
                output_grid[r, c] = container['color']

    # b. Fill internal regions
    for region_coords_fs, region_data in internal_regions_map.items():
        fill_color = region_data['fill_color']
        if fill_color is not None:
            for r, c in region_coords_fs:
                 if 0 <= r < height and 0 <= c < width:
                    output_grid[r, c] = fill_color

    return output_grid.tolist()