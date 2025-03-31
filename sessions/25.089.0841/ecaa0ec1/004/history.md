
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 8 1 8 0 0 0 0
0 0 0 1 8 8 0 0 0 0
0 4 0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 1 0 0 0 0
0 0 0 1 8 1 0 0 0 0
0 0 0 8 1 1 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 4 0 1 1 1 0 0 0 0
0 0 0 8 1 8 0 0 0 0
0 0 0 8 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 1 8 1 0 0 0 0
0 0 0 1 1 1 0 0 0 0
0 0 0 1 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 1 1 1 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0
0 0 0 0 1 8 1 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 8 1 0 0 0 0
0 0 0 0 8 8 1 0 0 0 0
0 0 0 0 1 8 1 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 8 1 8 0 0 0
0 0 0 0 8 1 8 0 0 0
0 0 0 0 1 1 8 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 8 1 1 0 0 0
0 0 0 0 8 1 8 0 0 0
0 0 0 0 8 1 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception of Task Elements:**

1.  **Input Grid Structure:** Each input grid contains a background of white pixels (0), several isolated yellow pixels (4), and a single complex object composed of blue (1) and azure (8) pixels.
2.  **Blue/Azure Object:** This object appears to be the primary element being transformed. In all examples, it occupies a 3x3 area.
3.  **Yellow Pixels:** These seem to act as control signals or parameters for the transformation. They are scattered around the blue/azure object.
4.  **Output Grid Structure:** The output grid contains the transformed blue/azure object, a single yellow pixel at a new location, and a white background. The original yellow pixels are gone.
5.  **Transformation:** The blue/azure object undergoes a rotation within its 3x3 space. The specific rotation seems dependent on the relative position of the *closest* yellow pixel in the input. The position of the *single* output yellow pixel seems related to the positions of the *second closest* yellow pixel(s) in the input.

**Analysis Summary:**

*   The core transformation is a rotation of the 3x3 blue/azure object.
*   The rotation type (90°, 180°, 270°, or 0°) is determined by the location of the *closest* input yellow pixel relative to the center of the blue/azure object.
    *   Closest Top-Left -> Rotate 270° clockwise (or 90° counter-clockwise)
    *   Closest Top-Right -> Rotate 90° clockwise
    *   Closest Bottom-Right -> Rotate 180° clockwise
    *   Closest Bottom-Left -> Rotate 0° (No rotation - inferred)
*   All input yellow pixels are removed.
*   A single new yellow pixel is placed in the output. Its location is the average position (row, column) of the input yellow pixel(s) that were *second closest* to the blue/azure object's center.

**YAML Facts:**


```yaml
elements:
  - object: background
    color: white
    value: 0
  - object: marker
    color: yellow
    value: 4
    role: control signal
    quantity: multiple in input, single in output
  - object: target
    color: [blue, azure]
    value: [1, 8]
    shape: 3x3 contiguous block
    role: transformed object
    quantity: single

relationships:
  - type: spatial
    description: Yellow markers are located relative to the target object.
  - type: distance
    description: Euclidean distance is calculated between the target object's center and each yellow marker.
  - type: ranking
    description: Yellow markers are ranked based on their distance to the target object (closest, second closest, etc.).

actions:
  - action: identify
    target: target object (blue/azure)
    result: location and 3x3 grid content
  - action: identify
    target: marker pixels (yellow)
    result: list of locations
  - action: calculate
    inputs: [target object center, marker locations]
    computation: Euclidean distance
    result: distance for each marker
  - action: find_minimum
    input: marker distances
    result: closest marker(s) location(s) and minimum distance
  - action: find_second_minimum
    input: marker distances
    result: second closest marker(s) location(s) and second minimum distance
  - action: determine_relative_direction
    inputs: [target object center, closest marker location]
    result: direction quadrant (TL, TR, BL, BR)
  - action: determine_rotation
    input: relative direction quadrant
    mapping:
      TL: 270 # degrees clockwise
      TR: 90
      BR: 180
      BL: 0
    result: rotation angle
  - action: rotate
    target: 3x3 grid of target object
    parameter: rotation angle
    result: rotated 3x3 grid
  - action: calculate_average_position
    input: locations of second closest marker(s)
    result: single output marker location (row, col)
  - action: construct_output
    elements:
      - rotated target object at original location
      - single output marker at calculated average position
      - background elsewhere

```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid, but set all non-white pixels to white (0).
2.  Find the connected component of blue (1) and azure (8) pixels (the target object). Determine its bounding box, which should be 3x3. Extract this 3x3 grid patch and note its top-left corner coordinates (origin\_row, origin\_col). Calculate the center coordinates of this 3x3 patch (center\_row, center\_col).
3.  Find the coordinates (row, col) of all yellow (4) pixels (the markers).
4.  For each marker, calculate the Euclidean distance between its coordinates (row, col) and the target object's center coordinates (center\_row, center\_col).
5.  Identify the marker(s) with the minimum distance. Assume there is a unique closest marker based on the examples. Let its coordinates be (closest\_row, closest\_col).
6.  Determine the relative direction of the closest marker from the target object's center:
    *   If `closest_row < center_row` and `closest_col < center_col`, direction is Top-Left (TL).
    *   If `closest_row < center_row` and `closest_col > center_col`, direction is Top-Right (TR).
    *   If `closest_row > center_row`
```python
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

```
```python
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
```
