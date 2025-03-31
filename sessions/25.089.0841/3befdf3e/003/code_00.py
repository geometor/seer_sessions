import numpy as np

"""
Expands a central rectangular object outwards by two layers, using the object's inner and outer colors.

The transformation identifies the single rectangular object in the input, which is composed of an outer frame color and an inner core color. It then creates an expanded version in the output grid. The expansion adds two layers around the original object: the layer immediately adjacent (orthogonal distance 1) is filled with the inner color, and the next layer (orthogonal distance 2) is filled with the outer color. The original object remains in place. The expansion only colors cells that were initially white (background color 0).
"""

def find_colors(grid):
    """Finds the unique non-zero colors in the grid."""
    return sorted(list(np.unique(grid[grid != 0])))

def find_bounding_box(grid):
    """Finds the bounding box (min_row, min_col, max_row, max_col) of non-zero pixels."""
    non_white_coords = np.argwhere(grid != 0)
    if non_white_coords.size == 0:
        return None
    min_r, min_c = non_white_coords.min(axis=0)
    max_r, max_c = non_white_coords.max(axis=0)
    return (min_r, min_c, max_r, max_c)

def determine_inner_outer(grid, colors, bbox):
    """
    Determines the inner and outer colors.
    Assumes the color at the top-left corner of the bounding box is the outer color.
    Handles cases where only one non-white color might be present (although the description implies two).
    """
    if len(colors) == 0:
        return None, None # No colors found
    
    min_r, min_c, _, _ = bbox
    outer_c = grid[min_r, min_c]
    
    if len(colors) == 1:
        # If only one color, it acts as both inner and outer for expansion
        # This might need adjustment based on specific task behavior for single-color objects
        inner_c = outer_c
    else:
        # If two colors, find the one that isn't the outer color
        inner_c = colors[0] if colors[1] == outer_c else colors[1]
        
    return inner_c, outer_c

def get_object_coords(grid):
    """Returns a list of (row, col) tuples for all non-zero pixels."""
    return [tuple(coord) for coord in np.argwhere(grid != 0)]

def min_manhattan_distance(point, coord_set):
    """Calculates the minimum Manhattan distance from a point to any coordinate in a set."""
    if not coord_set:
        return float('inf') # Or handle as appropriate if the set can be empty
    r1, c1 = point
    min_dist = float('inf')
    for r2, c2 in coord_set:
        dist = abs(r1 - r2) + abs(c1 - c2)
        min_dist = min(min_dist, dist)
    return min_dist

def transform(input_grid):
    """
    Applies the two-layer expansion transformation based on distance to the original object.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # 1. Identify the object and its properties
    non_white_colors = find_colors(input_np)
    object_coords = get_object_coords(input_np)

    if not object_coords: # No object found
        return input_grid # Return original grid if no object

    bbox = find_bounding_box(input_np) 
    
    # Handle cases where finding colors/bbox might fail or be inconsistent
    if not non_white_colors or bbox is None:
         return input_grid # Should not happen if object_coords is not empty, but safe check

    # Expecting two colors based on examples, but handle single color case.
    # The description implies two colors, adjust if single-color behavior differs.
    if len(non_white_colors) > 2:
        # Unexpected number of colors, return original grid or raise error
        print(f"Warning: Expected 1 or 2 non-white colors, found {len(non_white_colors)}. Returning original grid.")
        return input_grid

    inner_color, outer_color = determine_inner_outer(input_np, non_white_colors, bbox)
    
    # 2. Initialize the output grid as a copy of the input
    output_np = np.copy(input_np)

    # 3. Iterate through all grid cells to potentially color them
    for r in range(rows):
        for c in range(cols):
            # Only consider coloring cells that are currently white (background)
            if output_np[r, c] == 0:
                # 4. Calculate the minimum orthogonal distance to the original object
                min_dist = min_manhattan_distance((r, c), object_coords)

                # 5. Apply coloring rules based on distance
                if min_dist == 1:
                    # Color with inner_color if distance is 1
                    output_np[r, c] = inner_color
                elif min_dist == 2:
                    # Color with outer_color if distance is 2
                    output_np[r, c] = outer_color
                    
    # 6. Return the modified grid as a list of lists
    return output_np.tolist()