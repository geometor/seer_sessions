import numpy as np
import math

"""
Identifies a 3x3 target object composed of blue (1) and azure (8) pixels and multiple yellow (4) marker pixels in the input grid.
The transformation involves rotating the 3x3 target object and placing a single yellow marker in the output grid.

1.  **Find Elements**: Locate the 3x3 bounding box of the blue/azure target object and find the coordinates of all yellow markers.
2.  **Calculate Distances**: Compute the Euclidean distance between the center pixel of the target object and each yellow marker.
3.  **Determine Closest Marker**: Identify the yellow marker closest to the target object's center.
4.  **Determine Rotation**: Based on the relative position (quadrant) of the closest marker to the target object's center, determine the clockwise rotation angle for the target object:
    *   Top-Left (TL): 270 degrees (k=3 clockwise, k=1 for np.rot90 CCW)
    *   Top-Right (TR): 90 degrees (k=1 clockwise, k=3 for np.rot90 CCW)
    *   Bottom-Left (BL): 0 degrees (k=0 clockwise, k=0 for np.rot90 CCW)
    *   Bottom-Right (BR): 180 degrees (k=2 clockwise, k=2 for np.rot90 CCW)
5.  **Find Second Closest Markers**: Identify the marker(s) with the second smallest distance to the target object's center.
6.  **Calculate Output Marker Position**: Compute the average row and column of the second closest marker(s). Round the result to the nearest integer coordinates.
7.  **Construct Output**: Create an output grid of the same size as the input, filled with white (0). Place the rotated target object at its original position. Place a single yellow marker (4) at the calculated average position.
"""

def find_target_object(grid):
    """Finds the 3x3 blue/azure object, returns its patch and top-left corner."""
    target_colors = {1, 8}
    coords = np.argwhere(np.isin(grid, list(target_colors)))
    if coords.shape[0] == 0:
        return None, None, None # No target found

    min_r, min_c = coords.min(axis=0)
    max_r, max_c = coords.max(axis=0)

    # Expecting a 3x3 bounding box
    if max_r - min_r != 2 or max_c - min_c != 2:
         # If not exactly 3x3, maybe logic needs adjustment, but for now assume 3x3
         print(f"Warning: Target object bounding box is not 3x3 ({max_r-min_r+1}x{max_c-min_c+1}). Using min/max bounds.")
         # Fallback or error? For now, proceed with bounding box
         # Let's assume the examples guarantee 3x3, raise error otherwise
         raise ValueError("Target object is not a 3x3 shape.")


    origin_row, origin_col = min_r, min_c
    patch = grid[origin_row:origin_row + 3, origin_col:origin_col + 3]
    center_row = origin_row + 1
    center_col = origin_col + 1
    
    return patch, (origin_row, origin_col), (center_row, center_col)

def find_markers(grid, marker_color=4):
    """Finds all pixels of a specific color."""
    return np.argwhere(grid == marker_color)

def calculate_distance(p1, p2):
    """Calculates Euclidean distance."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.zeros_like(input_np) # Initialize with white (0)

    # 1. Find the target object and its properties
    target_patch, target_origin, target_center = find_target_object(input_np)
    if target_patch is None:
        # Handle case where no target object is found if necessary
        # For this problem, assume target always exists per examples
        print("Warning: No target object found.")
        return output_grid.tolist() # Return empty grid or copy of input?

    origin_row, origin_col = target_origin
    center_row, center_col = target_center

    # 2. Find markers
    marker_coords = find_markers(input_np, 4)
    if marker_coords.shape[0] == 0:
        print("Warning: No markers found.")
        # Place the unrotated object if no markers? Examples have markers.
        # Place original patch back for now if no markers.
        output_grid[origin_row:origin_row+3, origin_col:origin_col+3] = target_patch
        return output_grid.tolist()

    # 3. Calculate distances from center to markers
    distances = []
    for r, c in marker_coords:
        dist = calculate_distance((r, c), target_center)
        distances.append({'pos': (r, c), 'dist': dist})

    # Sort by distance
    distances.sort(key=lambda x: x['dist'])

    # 4. Determine closest marker and rotation
    closest_marker = distances[0]
    closest_row, closest_col = closest_marker['pos']

    # Determine relative quadrant and rotation amount (for np.rot90 CCW)
    if closest_row < center_row and closest_col < center_col: # TL
        k_rot = 1 # 270 CW -> 90 CCW
    elif closest_row < center_row and closest_col >= center_col: # TR
        k_rot = 3 # 90 CW -> 270 CCW
    elif closest_row >= center_row and closest_col < center_col: # BL
        k_rot = 0 # 0 CW -> 0 CCW
    else: # BR (closest_row >= center_row and closest_col >= center_col)
        k_rot = 2 # 180 CW -> 180 CCW

    # Rotate the target patch
    rotated_patch = np.rot90(target_patch, k=k_rot)

    # 5. Find second closest markers
    if len(distances) > 1:
        min_dist = distances[0]['dist']
        # Find the first distance strictly greater than the minimum
        second_dist_val = -1
        for d in distances:
            # Use tolerance for float comparison
            if d['dist'] > min_dist + 1e-9: 
                second_dist_val = d['dist']
                break
        
        second_closest_markers = []
        if second_dist_val != -1:
             # Collect all markers with distance close to second_dist_val
            for d in distances:
                 if abs(d['dist'] - second_dist_val) < 1e-9:
                     second_closest_markers.append(d['pos'])
    else:
        # Edge case: only one marker exists. Output marker position undefined by examples.
        # Let's place it at the original marker's position for lack of better rule.
        second_closest_markers = [closest_marker['pos']]


    # 6. Calculate output marker position (average of second closest)
    if second_closest_markers:
        avg_row = np.mean([pos[0] for pos in second_closest_markers])
        avg_col = np.mean([pos[1] for pos in second_closest_markers])
        # Round to nearest integer for grid coordinates
        output_marker_row = int(round(avg_row))
        output_marker_col = int(round(avg_col))
    else:
        # If somehow no second closest markers were found (e.g. all markers equidistant)
        # Default behavior? Place marker at center? Or original closest? Let's use closest.
         output_marker_row, output_marker_col = closest_row, closest_col


    # 7. Construct Output Grid
    # Place rotated patch
    output_grid[origin_row:origin_row+3, origin_col:origin_col+3] = rotated_patch
    
    # Place the single output marker (ensure within bounds)
    if 0 <= output_marker_row < height and 0 <= output_marker_col < width:
        output_grid[output_marker_row, output_marker_col] = 4
    else:
        print(f"Warning: Calculated output marker position ({output_marker_row}, {output_marker_col}) is out of bounds.")


    return output_grid.tolist()
