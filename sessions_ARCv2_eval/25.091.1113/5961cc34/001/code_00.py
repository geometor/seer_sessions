import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify an "activation column" defined by the vertical alignment of a unique yellow (4) pixel above red (2) pixels in the input grid.
2. Find all distinct contiguous objects made of blue (1) pixels.
3. Identify which blue objects are "activated" by having at least one pixel in the activation column.
4. For each activated blue object:
    a. Identify all its constituent pixel coordinates.
    b. Identify any green (3) pixels in the input grid that are adjacent (including diagonally) to any pixel of the activated blue object. These green pixel locations define "holes".
    c. Fill the locations of the activated blue object's pixels in the output grid with red (2), *except* for the locations identified as holes, which remain the background color (azure 8).
5. The output grid starts as all background color (azure 8), and only the filled activated shapes (minus holes) appear in the final output. All other original input elements are replaced by the background color.
"""

def find_objects(grid, color):
    """Finds all contiguous objects of a given color in the grid."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    # Check neighbors (orthogonal)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                objects.append(obj_coords)
    return objects

def get_adjacent_coords(grid_shape, coords, include_diagonal=True):
    """Gets all unique adjacent coordinates for a set of coordinates."""
    height, width = grid_shape
    adjacent_set = set()
    
    delta = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ] if include_diagonal else [
                 (-1, 0),
        ( 0, -1),          ( 0, 1),
                 ( 1, 0),
    ]

    for r, c in coords:
        for dr, dc in delta:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                adjacent_set.add((nr, nc))
                
    return adjacent_set


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid = np.array(input_grid, dtype=int)
    height, width = input_grid.shape
    
    # Define colors
    background_color = 8 # azure
    shape_color = 1      # blue
    hole_marker_color = 3 # green
    activation_marker_color = 4 # yellow
    fill_color = 2       # red

    # Initialize output_grid with background color
    output_grid = np.full_like(input_grid, background_color)

    # 1. Find the activation column
    activation_col = -1
    yellow_pixels = np.where(input_grid == activation_marker_color)
    if len(yellow_pixels[0]) > 0:
        # Assuming only one yellow pixel as per observations
        activation_col = yellow_pixels[1][0] 
        # We could add a check here to ensure red pixels are below it if needed
        # red_check = np.where((input_grid == fill_color) & (np.arange(width) == activation_col))
        # if not np.any(red_check[0] > yellow_pixels[0][0]):
             # activation_col = -1 # Invalidate if no red below

    # If no valid activation column found, return the empty grid
    if activation_col == -1:
        # This handles cases where the yellow marker might be missing, though not seen in examples
        return output_grid.tolist() 

    # 2. Find all blue objects
    blue_objects = find_objects(input_grid, shape_color)
    
    # Find all green pixel locations (potential holes)
    green_pixels = set(zip(*np.where(input_grid == hole_marker_color)))

    # 3. Identify activated objects and determine holes
    activated_objects_coords = []
    hole_coords_map = {} # Store holes per object index

    for idx, blue_obj_coords in enumerate(blue_objects):
        is_activated = False
        for r, c in blue_obj_coords:
            if c == activation_col:
                is_activated = True
                break
        
        if is_activated:
            activated_objects_coords.append(blue_obj_coords)
            
            # 4b. Find hole coordinates for this activated object
            object_holes = set()
            # Get coordinates adjacent to the blue object
            adj_to_blue_obj = get_adjacent_coords((height, width), blue_obj_coords, include_diagonal=True)
            
            # Include the object's own coordinates as potential locations for green markers
            potential_hole_locations = adj_to_blue_obj.union(blue_obj_coords)
            
            # Check which green pixels are in these potential locations
            for green_coord in green_pixels:
                if green_coord in potential_hole_locations:
                     object_holes.add(green_coord)
            hole_coords_map[idx] = object_holes # Note: Using original index, but only storing for activated ones

    # 4c & 5. Fill activated shapes in the output grid, respecting holes
    processed_indices = set() # Keep track of which objects have been processed
    for idx, blue_obj_coords in enumerate(blue_objects):
        is_activated = False
        for r, c in blue_obj_coords:
            if c == activation_col:
                is_activated = True
                break
        
        if is_activated:
            holes_for_this_object = hole_coords_map.get(idx, set()) # Get holes for this object
            for r, c in blue_obj_coords:
                if (r, c) not in holes_for_this_object:
                    output_grid[r, c] = fill_color


    return output_grid.tolist()