import numpy as np
import math

"""
Identifies a 3x3 target object composed of blue (1) and azure (8) pixels and multiple yellow (4) marker pixels in the input grid.
The transformation involves rotating the 3x3 target object and placing a single yellow marker in the output grid based on marker distances and positions relative to the target object's center.

1.  Initialize an output grid of the same dimensions as the input, filled entirely with the background color (white, 0).
2.  Identify the 3x3 patch containing the blue (1) and azure (8) pixels (the target object). Record its 3x3 pixel data, its top-left corner coordinates (origin_row, origin_col), and calculate its center coordinates (center_row = origin_row + 1, center_col = origin_col + 1).
3.  Find the coordinates (row, col) of all yellow (4) pixels (the markers).
4.  Calculate the Euclidean distance between the target object's center coordinates and the coordinates of each marker. Store these distances along with their corresponding marker coordinates.
5.  Sort the markers based on their calculated distance to the target center in ascending order.
6.  Identify the marker with the minimum distance (the closest marker). Let its coordinates be (closest_row, closest_col).
7.  Determine the relative direction quadrant of the closest marker with respect to the target center:
    *   Top-Left (TL): closest_row < center_row and closest_col < center_col
    *   Top-Right (TR): closest_row < center_row and closest_col >= center_col
    *   Bottom-Left (BL): closest_row >= center_row and closest_col < center_col
    *   Bottom-Right (BR): closest_row >= center_row and closest_col >= center_col
8.  Select the counter-clockwise rotation parameter `k` for numpy.rot90 based on the relative direction:
    *   If direction is TL or TR, set `k = 1` (90 degrees CCW).
    *   If direction is BR, set `k = 2` (180 degrees CCW).
    *   If direction is BL, set `k = 0` (0 degrees CCW).
9.  Rotate the extracted 3x3 target object patch counter-clockwise `k` times.
10. Place the rotated 3x3 target object patch onto the output grid at the original top-left coordinates (origin_row, origin_col).
11. Identify all markers that share the second smallest unique distance to the target center. Find the smallest distance value in the sorted list that is strictly greater than the minimum distance; collect all markers matching this second distance value.
12. Calculate the average row and average column of these second-closest markers. Round both averages to the nearest integer to get the output marker coordinates (output_marker_row, output_marker_col).
    *   *Edge Case Handling:* If there are fewer than two unique distances among markers (e.g., only one marker exists, or all markers are equidistant), use the coordinates of the closest marker as the output marker coordinates.
13. Place a single yellow (4) pixel on the output grid at the calculated (output_marker_row, output_marker_col), ensuring it's within bounds.
14. Return the final output grid.
"""

def find_target_object(grid):
    """Finds the 3x3 blue/azure object, returns its patch, origin, and center."""
    target_colors = {1, 8} # Blue and Azure
    coords = np.argwhere(np.isin(grid, list(target_colors)))
    
    # Check if any target pixels were found
    if coords.shape[0] == 0:
        return None, None, None 

    min_r, min_c = coords.min(axis=0)
    max_r, max_c = coords.max(axis=0)

    # Check if the bounding box is exactly 3x3
    if max_r - min_r != 2 or max_c - min_c != 2:
        # The task logic derived relies on a 3x3 object for center calculation and rotation
        print(f"Warning: Target object bounding box is not 3x3 ({max_r-min_r+1}x{max_c-min_c+1}). Cannot proceed.")
        return None, None, None 

    origin_row, origin_col = min_r, min_c
    patch = grid[origin_row:origin_row + 3, origin_col:origin_col + 3]
    # Center is the middle pixel of the 3x3 patch
    center_row = origin_row + 1
    center_col = origin_col + 1
    
    return patch, (origin_row, origin_col), (center_row, center_col)

def find_markers(grid, marker_color=4):
    """Finds all pixels of a specific color (markers)."""
    return np.argwhere(grid == marker_color)

def calculate_distance(p1, p2):
    """Calculates Euclidean distance between two points (row, col)."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

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
        print("Error: Target object not found or not 3x3.")
        return output_grid.tolist() 

    origin_row, origin_col = target_origin
    center_row, center_col = target_center

    # 3. Find markers (yellow pixels)
    marker_coords = find_markers(input_np, 4)
    
    # If no markers are found, place the original (unrotated) target object and return
    if marker_coords.shape[0] == 0:
        print("Warning: No markers found. Placing original object.")
        output_grid[origin_row:origin_row+3, origin_col:origin_col+3] = target_patch
        return output_grid.tolist()

    # 4. Calculate distances from target center to each marker
    distances = []
    for r, c in marker_coords:
        dist = calculate_distance((r, c), target_center)
        # Round distance for more robust comparison later
        distances.append({'pos': (r, c), 'dist': round(dist, 8)}) 

    # 5. Sort markers by distance (ascending)
    distances.sort(key=lambda x: x['dist'])

    # 6. Identify the closest marker and its distance
    closest_marker = distances[0]
    closest_row, closest_col = closest_marker['pos']
    min_dist = closest_marker['dist']

    # 7. Determine the relative direction (quadrant) of the closest marker
    is_top = closest_row < center_row
    is_left = closest_col < center_col

    # 8. Select rotation parameter k based on the quadrant (for np.rot90 CCW)
    if is_top and is_left: # Top-Left (TL)
        k_rot = 1
    elif is_top and not is_left: # Top-Right (TR)
        k_rot = 1
    elif not is_top and is_left: # Bottom-Left (BL)
        k_rot = 0
    else: # Bottom-Right (BR)
        k_rot = 2

    # 9. Rotate the target patch
    rotated_patch = np.rot90(target_patch, k=k_rot)

    # 10. Place the rotated patch onto the output grid
    output_grid[origin_row:origin_row+3, origin_col:origin_col+3] = rotated_patch

    # 11. Identify the second closest markers
    second_closest_markers_pos = []
    second_dist_val = -1
    # Find the first distance value strictly greater than the minimum distance
    for d in distances:
        if d['dist'] > min_dist: 
            second_dist_val = d['dist']
            break
            
    # If a second distinct distance exists, find all markers at that distance
    if second_dist_val != -1:
        for d in distances:
             # Compare rounded distances
             if d['dist'] == second_dist_val:
                 second_closest_markers_pos.append(d['pos'])

    # 12. Calculate the position for the single output marker
    output_marker_pos = None
    if second_closest_markers_pos: 
        # If second closest markers were found, average their positions
        avg_row = np.mean([pos[0] for pos in second_closest_markers_pos])
        avg_col = np.mean([pos[1] for pos in second_closest_markers_pos])
        # Round to nearest integer for grid coordinates
        output_marker_pos = (int(round(avg_row)), int(round(avg_col)))
    else:
        # Edge Case: If no distinct second distance exists (e.g., only 1 marker, or all markers equidistant)
        # Use the position of the closest marker as the default
        print("Warning: No distinct second closest markers found. Using closest marker position for output.")
        output_marker_pos = closest_marker['pos'] 

    # 13. Place the single yellow output marker
    output_marker_row, output_marker_col = output_marker_pos
    # Check if the calculated position is within the grid boundaries
    if 0 <= output_marker_row < height and 0 <= output_marker_col < width:
        output_grid[output_marker_row, output_marker_col] = 4 # Yellow color
    else:
        # Log a warning if the position is out of bounds
        print(f"Warning: Calculated output marker position ({output_marker_row}, {output_marker_col}) is out of bounds.")

    # 14. Return the final output grid as a list of lists
    return output_grid.tolist()