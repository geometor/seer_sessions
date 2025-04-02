import numpy as np
from scipy.ndimage import label

"""
Identifies the largest connected component of a non-background color (main object) 
in the input grid. Finds all enclosed regions (holes) of the background color (0) 
that are fully enclosed by this main object. 

The filling logic depends on the number of internal holes found:
- If exactly one internal hole is found, it is filled with the main object's color.
- If multiple internal holes are found:
    - The sizes (pixel counts) of all internal holes are determined.
    - If there is a unique largest hole among them, all *other* internal holes are filled.
    - If there is a tie for the largest hole size, *all* internal holes are filled.
- If no internal holes are found, the grid remains unchanged.
"""

def get_neighbors(coords, grid_shape):
    """ 
    Gets the set of unique orthogonal neighbor coordinates for a given set of coordinates.
    
    Args:
        coords (np.array): A Nx2 array of coordinates (row, col).
        grid_shape (tuple): The (height, width) of the grid.

    Returns:
        set: A set of unique neighbor coordinates (row, col) tuples.
    """
    neighbors = set()
    H, W = grid_shape
    coord_set = set(tuple(coord) for coord in coords) # For quick checking if neighbor is part of the original set

    for r, c in coords:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Orthogonal neighbors
            nr, nc = r + dr, c + dc
            # Check bounds and if the neighbor is not part of the original component
            if 0 <= nr < H and 0 <= nc < W and (nr, nc) not in coord_set:
                neighbors.add((nr, nc))
    return neighbors

def get_component_details(labeled_array, label_idx):
    """Gets coordinates and size of a specific component label."""
    coords = np.argwhere(labeled_array == label_idx)
    size = len(coords)
    return coords, size

def transform(input_grid):
    """
    Applies the hole-filling transformation based on the number and size of holes.
    """
    output_grid = np.copy(input_grid)
    H, W = input_grid.shape
    background_color = 0

    # 1. Find all connected components of non-background colors.
    labeled_objects, num_objects = label(input_grid != background_color)

    # Handle case with no non-background objects
    if num_objects == 0:
        return output_grid

    # 2. Determine the largest connected component (main object).
    object_sizes = []
    for i in range(1, num_objects + 1):
        coords, size = get_component_details(labeled_objects, i)
        if size > 0:
            object_sizes.append({'label': i, 'size': size, 'coords': coords})

    if not object_sizes: # Should not happen if num_objects > 0, but safety check
         return output_grid
         
    main_object_info = max(object_sizes, key=lambda item: item['size'])
    main_object_label = main_object_info['label']
    main_object_coords_arr = main_object_info['coords']
    main_object_coords_set = set(tuple(coord) for coord in main_object_coords_arr)
    main_object_color = input_grid[main_object_coords_arr[0, 0], main_object_coords_arr[0, 1]]

    # 3. Find all connected components of the background color.
    labeled_background, num_bg_components = label(input_grid == background_color)

    # 4. Identify the 'outer' background component (touching border or largest).
    outer_background_label = 0
    border_labels = set(labeled_background[0, :]) | \
                    set(labeled_background[-1, :]) | \
                    set(labeled_background[:, 0]) | \
                    set(labeled_background[:, -1])
    border_labels.discard(0) # Remove the 0 label if present

    if border_labels:
        # Typically there's only one background component touching the border
        outer_background_label = min(border_labels) # Take the first one found
    elif num_bg_components > 0:
        # If no background touches border, find the largest background component
        bg_sizes = []
        for i in range(1, num_bg_components + 1):
            coords, size = get_component_details(labeled_background, i)
            if size > 0:
                 bg_sizes.append({'label': i, 'size': size})
        if bg_sizes:
             outer_background_label = max(bg_sizes, key=lambda item: item['size'])['label']
    # If outer_background_label is still 0, means no background components found.

    # 5. Identify internal holes enclosed by the main object.
    internal_holes = [] 
    for i in range(1, num_bg_components + 1):
        # Skip the outer background component
        if i == outer_background_label:
            continue 
            
        bg_coords, hole_size = get_component_details(labeled_background, i)
        if hole_size == 0: continue # Should not happen with labels > 0

        # Check if this component is fully enclosed by the main object
        is_enclosed_by_main = True
        neighbor_coords = get_neighbors(bg_coords, (H, W))

        if not neighbor_coords: # An isolated background pixel not next to anything? Unlikely for a hole.
            is_enclosed_by_main = False

        for neighbor_coord in neighbor_coords:
            # If neighbor is NOT part of the main object, it's not enclosed
            if neighbor_coord not in main_object_coords_set:
                 is_enclosed_by_main = False
                 break 
                 
        if is_enclosed_by_main:
            internal_holes.append({'label': i, 'size': hole_size, 'coords': bg_coords})

    # 6. Determine which holes to fill based on the rules.
    num_internal_holes = len(internal_holes)
    holes_to_fill_coords = [] # List to store coordinates of holes to be filled

    if num_internal_holes == 1:
        # Fill the single hole
        holes_to_fill_coords.append(internal_holes[0]['coords'])
    elif num_internal_holes > 1:
        # Multiple holes: check sizes
        hole_sizes = [h['size'] for h in internal_holes]
        max_hole_size = max(hole_sizes)
        max_size_count = hole_sizes.count(max_hole_size)
        
        if max_size_count == 1:
            # Unique largest: fill all EXCEPT the largest
            for hole in internal_holes:
                if hole['size'] != max_hole_size:
                    holes_to_fill_coords.append(hole['coords'])
        else:
            # Tie for largest: fill ALL internal holes
            for hole in internal_holes:
                holes_to_fill_coords.append(hole['coords'])

    # 7. Fill the selected holes in the output grid.
    for coords_array in holes_to_fill_coords:
        for r, c in coords_array:
            # Double check bounds just in case, though get_component_details should be correct
            if 0 <= r < H and 0 <= c < W:
                output_grid[r, c] = main_object_color

    return output_grid