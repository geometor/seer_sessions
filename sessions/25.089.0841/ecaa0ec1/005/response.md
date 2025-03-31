```python
import numpy as np
import math

"""
Transforms an input grid based on the relative positions of a 3x3 target object (blue/azure) and multiple yellow markers.

1.  Locates the 3x3 target object and calculates its center.
2.  Locates all yellow markers.
3.  Calculates the Euclidean distance and relative quadrant (TL, TR, BL, BR) of each marker from the target's center.
4.  Sorts markers by distance.
5.  Determines a rotation amount (k * 90 degrees counter-clockwise) for the target object based on the quadrant of the closest marker. If the closest marker is in the Top-Right quadrant, the quadrants of the second-closest marker(s) are used to disambiguate the rotation (k=1 if second-closest are Left; k=3 if second-closest are Right).
6.  Rotates the target object.
7.  Calculates the position for a single output yellow marker by averaging the coordinates of the second-closest input marker(s) and rounding. If no second-closest markers exist, the closest marker's position is used.
8.  Constructs the output grid containing the rotated target object at its original location and the single output yellow marker at its calculated position, against a white background.
"""

# --- Helper Functions ---

def find_target_object(grid):
    """
    Finds the 3x3 object composed of blue (1) and azure (8) pixels.
    Returns its patch, top-left origin coordinates, and center coordinates.
    Returns None for any value if the object is not found or not exactly 3x3.
    """
    target_colors = {1, 8} # Blue and Azure
    coords = np.argwhere(np.isin(grid, list(target_colors)))
    
    # Check if any target pixels were found
    if coords.shape[0] == 0:
        print("Debug: No target pixels found.")
        return None, None, None 

    min_r, min_c = coords.min(axis=0)
    max_r, max_c = coords.max(axis=0)

    # Check if the bounding box is exactly 3x3
    if max_r - min_r != 2 or max_c - min_c != 2:
        print(f"Debug: Target bounding box is not 3x3 ({max_r-min_r+1}x{max_c-min_c+1}).")
        return None, None, None 

    origin = (min_r, min_c)
    patch = grid[min_r:min_r + 3, min_c:min_c + 3]
    # Center is the middle pixel of the 3x3 patch
    center = (min_r + 1, min_c + 1)
    
    return patch, origin, center

def find_markers(grid, marker_color=4):
    """Finds all pixels of a specific color (markers). Returns list of (row, col) tuples."""
    return [tuple(coord) for coord in np.argwhere(grid == marker_color)]

def calculate_distance(p1, p2):
    """Calculates Euclidean distance between two points (row, col)."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_quadrant(pos, center):
    """Determines the quadrant (TL, TR, BL, BR) of a position relative to a center."""
    r, c = pos
    cr, cc = center
    if r < cr and c < cc: return "TL"
    if r < cr and c >= cc: return "TR"
    if r >= cr and c < cc: return "BL"
    if r >= cr and c >= cc: return "BR"
    # Should not happen if pos != center
    print(f"Warning: Could not determine quadrant for pos {pos} relative to center {center}")
    return "Unknown" 

def calculate_distances_and_quadrants(marker_coords, center):
    """Calculates distance and quadrant for each marker relative to the center."""
    details = []
    for pos in marker_coords:
        dist = calculate_distance(pos, center)
        quad = get_quadrant(pos, center)
        # Round distance for robust comparison
        details.append({'pos': pos, 'dist': round(dist, 8), 'quad': quad})
    return details

def determine_rotation_k(closest_marker_detail, second_closest_marker_details):
    """Determines the rotation parameter k based on closest and second closest marker quadrants."""
    closest_quad = closest_marker_detail['quad']
    
    if closest_quad == "TL":
        return 1
    elif closest_quad == "BL":
        return 0
    elif closest_quad == "BR":
        return 2
    elif closest_quad == "TR":
        # Disambiguate based on second closest markers
        if not second_closest_marker_details:
             print("Warning: Closest marker in TR, but no second closest markers found. Defaulting k=1.")
             return 1 # Default based on example 2 trend? Or maybe k=0? Let's use 1.

        all_second_left = all(m['quad'] in ["TL", "BL"] for m in second_closest_marker_details)
        all_second_right = all(m['quad'] in ["TR", "BR"] for m in second_closest_marker_details)

        if all_second_left:
            return 1
        elif all_second_right:
            return 3
        else:
            # Mixed second closest quadrants when closest is TR - undefined by examples.
            print("Warning: Closest marker in TR, second closest markers have mixed L/R quadrants. Defaulting k=1.")
            return 1 # Defaulting to the more common TR case (k=1).
    else:
        # Unknown quadrant for closest marker
        print(f"Warning: Unknown quadrant '{closest_quad}' for closest marker. Defaulting k=0.")
        return 0

def calculate_output_marker_position(closest_marker_detail, second_closest_marker_details):
    """Calculates the output marker position."""
    if second_closest_marker_details:
        # Average the positions of the second closest markers
        avg_row = np.mean([m['pos'][0] for m in second_closest_marker_details])
        avg_col = np.mean([m['pos'][1] for m in second_closest_marker_details])
        # Round to nearest integer for grid coordinates
        return (int(round(avg_row)), int(round(avg_col)))
    else:
        # Fallback: use the position of the closest marker
        print("Debug: No distinct second closest markers found. Using closest marker position for output.")
        return closest_marker_detail['pos']

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # 1. Initialize output grid with background color (white)
    output_grid = np.zeros_like(input_np) 

    # 2. Find the target object and its properties
    target_patch, target_origin, target_center = find_target_object(input_np)
    
    # If no valid target object found, return the empty grid
    if target_patch is None:
        print("Error: Target object not found or not valid (3x3). Returning empty grid.")
        return output_grid.tolist() 
    origin_row, origin_col = target_origin

    # 3. Find markers (yellow pixels)
    marker_coords = find_markers(input_np, 4)
    
    # If no markers are found, place the original (unrotated) target object and return
    if not marker_coords:
        print("Warning: No markers found. Placing original object and returning.")
        output_grid[origin_row:origin_row+3, origin_col:origin_col+3] = target_patch
        return output_grid.tolist()

    # 4. Calculate distances and quadrants for markers
    marker_details = calculate_distances_and_quadrants(marker_coords, target_center)

    # 5. Sort markers by distance
    marker_details.sort(key=lambda x: x['dist'])

    # 6. Identify closest marker(s)
    closest_marker_detail = marker_details[0]
    min_dist = closest_marker_detail['dist']

    # 7. Identify second closest marker(s)
    second_closest_marker_details = []
    second_dist_val = -1
    for detail in marker_details:
        if detail['dist'] > min_dist: 
            second_dist_val = detail['dist']
            break
    if second_dist_val != -1:
        for detail in marker_details:
             if detail['dist'] == second_dist_val:
                 second_closest_marker_details.append(detail)

    # 8. Determine rotation parameter k
    k_rot = determine_rotation_k(closest_marker_detail, second_closest_marker_details)

    # 9. Rotate the target patch
    rotated_patch = np.rot90(target_patch, k=k_rot)

    # 10. Place the rotated patch onto the output grid
    output_grid[origin_row:origin_row+3, origin_col:origin_col+3] = rotated_patch

    # 11. Calculate the position for the single output marker
    output_marker_pos = calculate_output_marker_position(closest_marker_detail, second_closest_marker_details)

    # 12. Place the single yellow output marker
    output_marker_row, output_marker_col = output_marker_pos
    # Check if the calculated position is within the grid boundaries
    if 0 <= output_marker_row < height and 0 <= output_marker_col < width:
        output_grid[output_marker_row, output_marker_col] = 4 # Yellow color
    else:
        # Log a warning if the position is out of bounds
        print(f"Warning: Calculated output marker position ({output_marker_row}, {output_marker_col}) is out of bounds.")

    # 13. Return the final output grid as a list of lists
    return output_grid.tolist()
```