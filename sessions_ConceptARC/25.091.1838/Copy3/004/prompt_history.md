
## train_1

**input:**
```
0 0 4 4 4 0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 1 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 4 4 4 0 0 0 0
```


**output:**
```
0 0 4 4 4 0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 4 0 0 0 0
0 0 1 0 1 0 1 0 0 1 0 1 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 3 3 3 3 3 0 0
0 0 0 0 4 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 4 0 0 0 0
0 0 4 4 4 0 0 0 0 4 4 4 0 0 0 0
```


## train_2

**input:**
```
6 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 7 0 0 0 0 0 0 0 0 0 0
3 4 7 0 0 0 6 6 0 0 0 0 0
3 0 7 0 0 0 0 0 0 0 0 0 0
3 4 7 0 0 0 0 0 7 0 0 0 0
4 0 0 0 0 0 0 0 7 0 0 0 0
0 4 0 0 0 0 0 0 7 0 0 0 0
0 0 6 6 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 7 0 0 0 0 0 0 0 0 0 0
3 4 7 0 0 0 6 6 0 0 0 0 0
3 0 7 0 0 0 0 0 0 0 0 0 0
3 4 7 0 0 0 3 0 7 0 0 0 0
4 0 0 0 0 0 3 4 7 0 0 0 0
0 4 0 0 0 0 3 0 7 0 0 0 0
0 0 6 6 0 0 3 4 7 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task based on the provided examples.

**Perception of the Elements**

1.  **Grid Structure:** The task operates on grids of pixels with different colors. The dimensions of the grids can vary.
2.  **Transformation Logic:** The core transformation seems to involve copying parts of the input grid to other locations within the grid to produce the output. The specific method of copying appears to depend on the width of the input grid.
3.  **Even Width Case (Example 1):**
    *   Input grid width is 16 (even).
    *   The output grid is formed by taking the input grid and overwriting its right half with a copy of its left half.
    *   The vertical line dividing the halves is exactly down the middle (between columns 7 and 8).
    *   Pixels from `(r, c)` where `c < width/2` are copied to `(r, c + width/2)`.
4.  **Odd Width Case (Example 2):**
    *   Input grid width is 13 (odd).
    *   The transformation involves identifying a specific "marker" object: a horizontal 1x2 block of magenta pixels (`[[6, 6]]`).
    *   The instance of this marker object closest to the geometric center of the grid determines a displacement vector (offset). The offset is simply the row and column index of the top-left pixel of this central marker.
    *   All other distinct objects (contiguous blocks of the same non-white color) in the input grid are copied.
    *   The copy destination for an object originally at `(r_obj, c_obj)` is `(r_obj + r_marker, c_obj + c_marker)`.
    *   Copies that would fall partially or fully outside the grid boundaries are clipped or ignored (only pixels landing within the grid are placed).
    *   The original content of the grid remains, and the copied objects are overlaid onto it. The marker object itself is *not* copied using the offset.
5.  **Object Definition:** An "object" seems to be a connected component of pixels sharing the same non-white color. Connectivity includes adjacent (horizontal/vertical) pixels.

**Facts (YAML)**


```yaml
task_type: object_copying
grid_properties:
  width_parity_dependent: true

rules:
  - condition: grid_width is even
    action: mirror_left_half_to_right
    details:
      - split_column: width / 2
      - source_columns: 0 to (width / 2) - 1
      - target_columns: (width / 2) to width - 1
      - transformation: output[r][c + width/2] = input[r][c]
      - overwrite: true (right half is completely replaced)

  - condition: grid_width is odd
    action: offset_copy_based_on_marker
    marker_object:
      shape: horizontal 1x2 block
      color: 6 (magenta)
      pixels: [[6, 6]]
    offset_determination:
      - find_all_instances: marker_object
      - calculate_grid_center: ( (height-1)/2, (width-1)/2 )
      - find_closest_marker: instance whose top-left (r_marker, c_marker) has minimum Euclidean distance to grid_center
      - offset_vector: (dr, dc) = (r_marker, c_marker)
    copy_process:
      - identify_all_source_objects: contiguous non-white pixel groups
      - exclude_object: the marker object used for offset determination
      - for_each_included_object:
        - source_location: top-left (r_obj, c_obj)
        - target_location: top-left (r_obj + dr, c_obj + dc)
        - copy_pixels: for each pixel (r_p, c_p) in the object, place its color at (r_p + dr, c_p + dc) in the output
        - boundary_check: only place pixels if target coordinates are within grid bounds (0 <= row < height, 0 <= col < width)
        - overwrite: true (copied pixels replace existing content at target locations)
    initial_state: output grid starts as a copy of the input grid
```


**Natural Language Program**

1.  Receive the input grid.
2.  Create the initial output grid as an identical copy of the input grid.
3.  Determine the width (`W`) and height (`H`) of the input grid.
4.  Check if the width `W` is even or odd.
5.  **If `W` is even:**
    a. Calculate the midpoint column index `Mid = W / 2`.
    b. For each row `r` from 0 to `H-1`:
    c. For each column `c` from 0 to `Mid-1`:
    d. Get the pixel value `P = input_grid[r][c]`.
    e. Set the pixel value in the output grid at `output_grid[r][c + Mid] = P`.
6.  **If `W` is odd:**
    a. Define the marker object as a horizontal 1x2 block of magenta pixels (`[[6, 6]]`).
    b. Find the coordinates `(r, c)` of the top-left pixel of all instances of the marker object in the input grid. Store these as a list of potential marker locations.
    c. If no marker objects are found, stop and return the initial output grid (which is a copy of the input).
    d. Calculate the geometric center of the grid: `center_r = (H - 1) / 2`, `center_c = (W - 1) / 2`.
    e. Find the marker location `(r_marker, c_marker)` from the list found in step 6b that has the minimum Euclidean distance to `(center_r, center_c)`. This `(r_marker, c_marker)` defines the copy offset `(dr, dc)`.
    f. Find all distinct connected objects of non-white pixels in the input grid. For each object, determine its color and the set of coordinates `{(r_p, c_p), ...}` it occupies. Also note its top-left coordinate `(r_obj, c_obj)`.
    g. For each object found in step 6f:
    h. Check if its top-left coordinate `(r_obj, c_obj)` is the same as the chosen marker's coordinate `(r_marker, c_marker)`.
    i. **If it is *not* the marker object:**
        i. For each pixel coordinate `(r_p, c_p)` belonging to this object:
```python
import numpy as np
from scipy.spatial.distance import euclidean
from collections import deque

"""
Transforms an input grid based on its width:

1. If the grid width is even:
   - The output grid is formed by copying the left half of the input grid onto the right half. The left half remains unchanged.

2. If the grid width is odd:
   - Identify a marker object: a horizontal 1x2 block of magenta pixels ([[6, 6]]).
   - Find the instance of this marker object whose top-left corner is closest to the geometric center of the grid. The coordinates (r_marker, c_marker) of this marker's top-left corner define an offset vector.
   - If no marker is found, the output is identical to the input.
   - Identify all distinct connected objects (contiguous blocks of the same non-white color) in the input grid.
   - For each object *except* the specific marker object used for the offset:
     - Copy the object to a new location in the output grid by adding the offset (r_marker, c_marker) to the coordinates of each pixel in the object.
     - Only pixels landing within the grid boundaries are placed.
     - Copied pixels overwrite the existing content at the target location. The original grid content and objects (including the marker) remain unless overwritten.
"""

def find_objects(grid, colors_to_ignore=[0]):
    """
    Finds all connected objects of the same color in the grid.

    Args:
        grid (np.array): The input grid.
        colors_to_ignore (list): List of color values to ignore (background).

    Returns:
        list: A list of tuples, where each tuple represents an object:
              (color, set_of_coordinates, top_left_coordinate).
              set_of_coordinates is a set of (row, col) tuples.
              top_left_coordinate is a tuple (min_row, min_col).
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color not in colors_to_ignore and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append((color, obj_coords, (min_r, min_c)))
    return objects

def find_pattern(grid, pattern):
    """
    Finds all occurrences of a given pattern in the grid.

    Args:
        grid (np.array): The input grid.
        pattern (np.array): The pattern to search for.

    Returns:
        list: A list of (row, col) tuples representing the top-left coordinates
              of found pattern instances.
    """
    grid_h, grid_w = grid.shape
    pattern_h, pattern_w = pattern.shape
    locations = []

    for r in range(grid_h - pattern_h + 1):
        for c in range(grid_w - pattern_w + 1):
            subgrid = grid[r:r+pattern_h, c:c+pattern_w]
            if np.array_equal(subgrid, pattern):
                locations.append((r, c))
    return locations

def transform(input_grid):
    """
    Applies the transformation rule based on grid width.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_np = np.copy(input_np) # Start with a copy

    # Check if width is even or odd
    if width % 2 == 0:
        # Even width: Mirror left half to right half
        mid = width // 2
        left_half = input_np[:, :mid]
        output_np[:, mid:] = left_half
    else:
        # Odd width: Offset copy based on marker
        marker_pattern = np.array([[6, 6]]) # Magenta 1x2 block
        marker_locations = find_pattern(input_np, marker_pattern)

        if not marker_locations:
            # No marker found, return the copy of the input
            return output_np.tolist()

        # Calculate grid center
        center_r = (height - 1) / 2.0
        center_c = (width - 1) / 2.0
        grid_center = (center_r, center_c)

        # Find the marker closest to the center
        closest_marker_loc = min(
            marker_locations,
            key=lambda loc: euclidean(loc, grid_center)
        )
        r_marker, c_marker = closest_marker_loc
        offset_dr, offset_dc = r_marker, c_marker

        # Find all objects
        objects = find_objects(input_np, colors_to_ignore=[0]) # Ignore white background

        # Iterate through objects and copy them with offset, skipping the chosen marker
        for color, coords, top_left_coord in objects:
            # Check if this object is the chosen marker
            is_marker = False
            # For a 1x2 marker, the top_left_coord is sufficient to identify it
            if top_left_coord == closest_marker_loc and color == 6: 
                 # Basic check, might need refinement if other magenta objects exist
                 # Let's be more specific: check if the object's pixels exactly match the marker pattern relative to top_left
                 obj_pixels_relative = {(r - top_left_coord[0], c - top_left_coord[1]) for r, c in coords}
                 marker_pixels_relative = {(0,0), (0,1)} # For [[6, 6]] pattern
                 if obj_pixels_relative == marker_pixels_relative:
                     is_marker = True

            if not is_marker:
                # Copy this object with offset
                for r_p, c_p in coords:
                    target_r = r_p + offset_dr
                    target_c = c_p + offset_dc

                    # Check grid boundaries
                    if 0 <= target_r < height and 0 <= target_c < width:
                        output_np[target_r, target_c] = color

    # Convert back to list of lists before returning
    return output_np.tolist()
```
```python
import numpy as np
from scipy.spatial.distance import euclidean
from collections import deque

"""
Transforms an input grid based on its width:

1. If the grid width is even:
   - The output grid is formed by copying the left half of the input grid onto the right half. 
   - The left half remains unchanged, and the original right half is overwritten.

2. If the grid width is odd:
   - Identify a marker object: a horizontal 1x2 block of magenta pixels ([[6, 6]]).
   - Find the instance of this marker object whose top-left corner is closest (using Euclidean distance) to the geometric center of the grid. 
   - The coordinates (r_marker, c_marker) of this marker's top-left corner define an offset vector.
   - If no such marker is found, the output is identical to the input.
   - Identify all distinct connected objects (contiguous blocks of the same non-white color) in the input grid using 4-connectivity (up, down, left, right).
   - For each identified object *except* the specific marker object instance used for the offset:
     - Copy the object to a new location in the output grid by adding the offset vector (r_marker, c_marker) to the coordinates of each pixel in the object.
     - Only pixels whose target coordinates land within the grid boundaries are placed.
     - Copied pixels overwrite the existing content at the target location. The original grid content and objects (including the marker itself) remain unless overwritten by a copied pixel.
"""

def find_objects(grid, colors_to_ignore=[0]):
    """
    Finds all connected objects of the same color in the grid using 4-connectivity.

    Args:
        grid (np.array): The input grid.
        colors_to_ignore (list): List of color values to ignore (e.g., background).

    Returns:
        list: A list of tuples, where each tuple represents an object:
              (color, set_of_coordinates, top_left_coordinate).
              set_of_coordinates is a set of (row, col) tuples.
              top_left_coordinate is a tuple (min_row, min_col).
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Check if the pixel is not ignored and not visited yet
            if color not in colors_to_ignore and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c # Track top-left for easy identification

                # Breadth-First Search (BFS) to find connected components
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within bounds, has the same color, and hasn't been visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store the found object
                objects.append((color, obj_coords, (min_r, min_c)))
    return objects

def find_pattern(grid, pattern):
    """
    Finds all occurrences of a given 2D pattern in the grid.

    Args:
        grid (np.array): The input grid.
        pattern (np.array): The 2D pattern (subgrid) to search for.

    Returns:
        list: A list of (row, col) tuples representing the top-left coordinates
              of found pattern instances.
    """
    grid_h, grid_w = grid.shape
    pattern_h, pattern_w = pattern.shape
    locations = []

    # Iterate through possible top-left positions for the pattern
    for r in range(grid_h - pattern_h + 1):
        for c in range(grid_w - pattern_w + 1):
            # Extract the subgrid matching the pattern's dimensions
            subgrid = grid[r:r+pattern_h, c:c+pattern_w]
            # Compare the subgrid with the pattern
            if np.array_equal(subgrid, pattern):
                locations.append((r, c))
    return locations

def transform(input_grid):
    """
    Applies the transformation rule based on the input grid's width.
    """
    # Convert input list of lists to a NumPy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    # Initialize the output grid as a copy of the input grid
    output_np = np.copy(input_np) 

    # --- Determine transformation based on width parity ---
    if width % 2 == 0:
        # --- Even Width: Mirror Left Half to Right Half ---
        
        # Calculate the column index splitting the grid in half
        mid = width // 2
        # Extract the left half of the input grid
        left_half = input_np[:, :mid]
        # Overwrite the right half of the output grid with the left half
        output_np[:, mid:] = left_half
        
    else:
        # --- Odd Width: Offset Copy Based on Central Marker ---
        
        # Define the marker pattern: a horizontal 1x2 block of magenta (6)
        marker_pattern = np.array([[6, 6]]) 
        # Find all locations where this pattern occurs
        marker_locations = find_pattern(input_np, marker_pattern)

        # If no marker is found, the output is just the copy of the input
        if not marker_locations:
            return output_np.tolist()

        # Calculate the geometric center of the grid
        center_r = (height - 1) / 2.0
        center_c = (width - 1) / 2.0
        grid_center = (center_r, center_c)

        # Find the marker instance closest to the grid center
        closest_marker_loc = min(
            marker_locations,
            key=lambda loc: euclidean(loc, grid_center) # Use Euclidean distance
        )
        # The offset vector is the coordinates of the closest marker's top-left pixel
        offset_dr, offset_dc = closest_marker_loc 

        # Find all distinct objects (connected components of non-white pixels)
        objects = find_objects(input_np, colors_to_ignore=[0]) # Ignore white (0)

        # Iterate through all found objects to perform the copy
        for color, coords, top_left_coord in objects:
            
            # --- Check if the current object is the specific marker used for the offset ---
            is_the_offset_marker = False
            # Check color and top-left coordinate first for efficiency
            if color == 6 and top_left_coord == closest_marker_loc:
                 # Verify the exact shape/pixels relative to top-left to be sure
                 obj_pixels_relative = {(r - top_left_coord[0], c - top_left_coord[1]) for r, c in coords}
                 marker_pixels_relative = {(0,0), (0,1)} # Relative coords for [[6, 6]] pattern
                 if obj_pixels_relative == marker_pixels_relative:
                     is_the_offset_marker = True

            # --- If it's NOT the offset marker, copy it ---
            if not is_the_offset_marker:
                # Iterate through each pixel of the object
                for r_p, c_p in coords:
                    # Calculate the target coordinates using the offset
                    target_r = r_p + offset_dr
                    target_c = c_p + offset_dc

                    # Check if the target coordinates are within the grid boundaries
                    if 0 <= target_r < height and 0 <= target_c < width:
                        # Place the object's pixel color at the target location in the output grid
                        output_np[target_r, target_c] = color

    # Convert the final NumPy array back to a list of lists before returning
    return output_np.tolist()
```
