
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 0 2 2 0 4 4 0 3 3 0
0 1 1 0 2 2 0 4 4 0 5 5 0
0 1 1 0 5 5 0 4 4 0 3 3 0
0 1 1 0 2 2 0 5 5 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 2 2 0 3 3 0 1 1 0
0 4 4 0 2 2 0 3 3 0 1 1 0
0 4 4 0 2 2 0 3 3 0 1 1 0
0 4 4 0 2 2 0 3 3 0 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 0 2 2 2 0 6 6 6 0 7 7 7
4 0 4 0 2 2 2 0 6 6 6 0 7 7 7
4 4 4 0 2 2 2 0 6 6 6 0 7 7 7
4 4 4 0 2 2 2 0 6 6 6 0 7 7 7
4 4 4 0 2 0 2 0 6 6 6 0 7 7 7
4 4 4 0 2 2 2 0 6 6 6 0 7 0 7
4 4 4 0 2 2 2 0 6 0 6 0 7 7 7
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
6 6 6 0 7 7 7 0 2 2 2 0 4 4 4
6 6 6 0 7 7 7 0 2 2 2 0 4 4 4
6 6 6 0 7 7 7 0 2 2 2 0 4 4 4
6 6 6 0 7 7 7 0 2 2 2 0 4 4 4
6 6 6 0 7 7 7 0 2 2 2 0 4 4 4
6 6 6 0 7 7 7 0 2 2 2 0 4 4 4
6 6 6 0 7 7 7 0 2 2 2 0 4 4 4
```

Okay, let's break down the transformation logic for this task.

**Perception of the Elements:**

1.  **Grid Structure:** Both input and output grids maintain the same dimensions. The background color, white (0), remains unchanged and acts as a separator between distinct shapes or objects.
2.  **Objects:** The core elements are distinct objects composed of connected non-white pixels. These objects are separated horizontally by columns of the white background color.
3.  **Object Types:** There appear to be two categories of objects based on their composition across the examples:
    *   **Type 1 (Train_1):** Objects contain exactly two non-white colors: gray (5) and one other 'primary' color (blue, red, yellow, or green). The shape is relatively solid.
    *   **Type 2 (Train_2):** Objects contain only one non-white color (yellow, red, magenta, or orange) but may contain internal "holes" represented by the white (0) background color.
4.  **Transformation:** The transformation modifies the colors of the pixels *within* each object, while preserving the object's overall shape, position, and any internal holes (white pixels within the object's boundary). The specific color change depends on the type of object.
5.  **Conditional Logic:** The presence or absence of the gray (5) color within an object dictates which color transformation rule is applied.

**Facts:**


```yaml
Grid:
  Properties:
    - Size: Unchanged between input and output.
    - Background: Color white (0) is preserved. Acts as a separator.
Objects:
  Definition: Connected components of non-white pixels (pixels with value > 0).
  Properties:
    - Pixels: The set of coordinates belonging to the component.
    - Has_Gray: Boolean flag, true if any pixel in the component has value gray (5).
    - Primary_Color:
        - If Has_Gray is true: The non-gray, non-white color within the component (assuming one primary color exists besides gray based on examples).
        - If Has_Gray is false: The single non-white color of the component.
    - Shape: Defined by the `Pixels` coordinates. Preserved in the output (including internal white/0 pixels).
Transformation:
  Type: Color substitution within objects.
  Rule: Conditional based on the `Has_Gray` property of the object.
  Mappings:
    - Rule_Gray_Present: # Applied if Has_Gray is true
        Input_Color: Blue (1) -> Output_Color: Yellow (4)
        Input_Color: Red (2) -> Output_Color: Red (2)
        Input_Color: Yellow (4) -> Output_Color: Green (3)
        Input_Color: Green (3) -> Output_Color: Blue (1)
    - Rule_Gray_Absent: # Applied if Has_Gray is false
        Input_Color: Yellow (4) -> Output_Color: Magenta (6)
        Input_Color: Red (2) -> Output_Color: Orange (7)
        Input_Color: Magenta (6) -> Output_Color: Red (2)
        Input_Color: Orange (7) -> Output_Color: Yellow (4)
Action:
  - Iterate through each identified object in the input grid.
  - Determine `Has_Gray` and `Primary_Color` for the object.
  - Select the appropriate transformation mapping (Rule_Gray_Present or Rule_Gray_Absent).
  - Determine the `Output_Color` by applying the selected mapping to the `Primary_Color`.
  - For every pixel coordinate within the object's `Pixels` set, change the color in the output grid at that coordinate to the determined `Output_Color`.
  - Pixels that were originally white (0), whether background or internal holes, remain white (0).
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct objects in the input grid. An object is a group of connected pixels with colors other than white (0).
3.  For each identified object:
    a.  Examine all pixels belonging to the object to check if any of them are gray (5).
    b.  Determine the object's 'primary color'. If gray (5) is present, the primary color is the *other* non-white color in the object. If gray (5) is absent, the primary color is the single non-white color composing the object.
    c.  Select the appropriate color transformation rule based on whether gray (5) was found:
        i.  **If gray (5) is present:** Use the mapping: Blue (1) becomes Yellow (4), Red (2) becomes Red (2), Yellow (4) becomes Green (3), Green (3) becomes Blue (1).
        ii. **If gray (5) is absent:** Use the mapping: Yellow (4) becomes Magenta (6), Red (2) becomes Orange (7), Magenta (6) becomes Red (2), Orange (7) becomes Yellow (4).
    d.  Apply the selected transformation rule to the object's primary color to find the target output color.
    e.  For every pixel coordinate that belongs to the current object in the input grid, update the corresponding pixel in the output grid to the calculated target output color. (This ensures both the primary color and the gray color pixels, if present, are updated).
4.  Return the modified output grid.
```python
import numpy as np
from collections import deque

"""
This program transforms an input grid into an output grid based on the colors within connected objects.

1.  Identifies distinct objects in the input grid. An object is a contiguous group of non-white (non-zero) pixels.
2.  For each object, it determines if the color gray (5) is present among its pixels.
3.  Based on the presence or absence of gray (5), it identifies a 'primary' color for the object:
    - If gray (5) is present, the primary color is the other non-white color in the object.
    - If gray (5) is absent, the primary color is the single non-white color composing the object.
4.  Applies a color transformation rule to the primary color to get a target output color. There are two separate rules: one for objects containing gray, and one for objects without gray.
    - Rule (Gray Present): Blue (1) -> Yellow (4), Red (2) -> Red (2), Yellow (4) -> Green (3), Green (3) -> Blue (1).
    - Rule (Gray Absent): Yellow (4) -> Magenta (6), Red (2) -> Orange (7), Magenta (6) -> Red (2), Orange (7) -> Yellow (4).
5.  Updates all pixels belonging to the original object in the output grid to this single target output color, preserving the object's shape and position.
6.  White (0) pixels (background or internal holes) remain unchanged.
"""

def find_objects(grid):
    """
    Finds connected components of non-background (non-zero) pixels in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'coords' (a set of (row, col) tuples) and 'colors'
              (a set of color values present in the object).
    """
    height, width = grid.shape
    visited = set()
    objects = []
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and (r, c) not in visited:
                # Found the start of a new object
                current_object_coords = set()
                current_object_colors = set()
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    row, col = q.popleft()
                    current_object_coords.add((row, col))
                    current_object_colors.add(grid[row, col])

                    # Check 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] != 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                if current_object_coords:
                    objects.append({
                        'coords': current_object_coords,
                        'colors': current_object_colors
                    })
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on object colors and presence of gray.

    Args:
        input_grid (np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Define the color transformation maps
    map_gray_present = {
        1: 4,  # Blue -> Yellow
        2: 2,  # Red -> Red
        4: 3,  # Yellow -> Green
        3: 1   # Green -> Blue
    }
    map_gray_absent = {
        4: 6,  # Yellow -> Magenta
        2: 7,  # Red -> Orange
        6: 2,  # Magenta -> Red
        7: 4   # Orange -> Yellow
    }

    # Find all objects in the input grid
    objects = find_objects(input_grid)

    # Process each object
    for obj in objects:
        coords = obj['coords']
        colors = obj['colors']
        
        # Check if gray (5) is present
        has_gray = 5 in colors

        primary_color = -1
        target_color = -1

        if has_gray:
            # Find the primary color (the one that's not 0 or 5)
            # Assuming exactly one primary color exists alongside gray based on examples
            primary_colors = [c for c in colors if c != 0 and c != 5]
            if primary_colors: # Should always be true if has_gray and object exists
                 primary_color = primary_colors[0]
                 # Apply the transformation rule for objects with gray
                 target_color = map_gray_present.get(primary_color, primary_color) # Default to itself if not in map
            else:
                # Handle edge case? E.g., an object made *only* of gray?
                # Based on examples, this doesn't seem to happen. Assume we find a primary.
                # If only gray existed, maybe it maps to itself? For now, stick to observed rules.
                # Let's assume primary_color must be found if gray is present. If not, something is wrong.
                # If object was ONLY gray, target_color would remain -1. We can add a fallback.
                if not primary_colors and colors == {5}:
                     target_color = 5 # Map gray-only object to gray? Or maybe another rule applies? Let's keep gray.
                     # However, based on task, this scenario doesn't occur.
                else:
                     # This case signifies an unexpected object composition (e.g. {0, 5})
                     # Defaulting to keep original color might be safest if primary unclear
                     # For now, assume the primary color is always identifiable per rules.
                     pass # target_color remains -1 initially

        else: # No gray color (5) in the object
            # Find the primary color (the single non-zero color)
            primary_colors = [c for c in colors if c != 0]
            if len(primary_colors) == 1: # Should be true for non-gray objects based on examples
                primary_color = primary_colors[0]
                # Apply the transformation rule for objects without gray
                target_color = map_gray_absent.get(primary_color, primary_color) # Default to itself if not in map
            else:
                # Handle edge case: multiple non-gray colors without gray present?
                # Not observed in examples. Assume single primary color if no gray.
                pass # target_color remains -1

        # Update the output grid for all pixels in this object
        if target_color != -1: # Ensure we found a valid transformation
            for r, c in coords:
                 # Check bounds just in case, though coords should be valid
                if 0 <= r < height and 0 <= c < width:
                    output_grid[r, c] = target_color
        # If target_color remained -1 (due to unexpected object composition),
        # the original colors in output_grid (copied from input) are preserved for that object.

    return output_grid
```
```python
import numpy as np
from collections import deque

"""
Transforms the input grid based on object colors and the presence of gray (5), filling internal holes.

1.  Identifies distinct objects in the input grid. An object consists of:
    *   A core set of connected non-white (non-zero) pixels ('Pixels').
    *   An optional set of enclosed white (0) pixels ('Internal_Holes') surrounded by the object's 'Pixels'.
2.  For each object, checks if gray (5) is present among its core pixels.
3.  Determines a 'primary color':
    *   If gray is present, it's the other non-white color.
    *   If gray is absent, it's the single non-white color.
4.  Applies one of two color transformation rules to the primary color based on gray's presence, yielding a 'target output color':
    *   Rule (Gray Present): Blue(1)->Yellow(4), Red(2)->Red(2), Yellow(4)->Green(3), Green(3)->Blue(1).
    *   Rule (Gray Absent): Yellow(4)->Magenta(6), Red(2)->Orange(7), Magenta(6)->Red(2), Orange(7)->Yellow(4).
5.  Updates the output grid by setting all pixels corresponding to the object's core ('Pixels') and its 'Internal_Holes' to the 'target output color'.
6.  External background pixels remain unchanged.
"""

def _find_objects(grid):
    """
    Finds connected components (objects) of non-background pixels and their internal holes.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'coords' (set of non-zero pixel coordinates),
              'internal_holes' (set of enclosed zero pixel coordinates),
              'colors' (set of non-zero color values), and 'has_gray' (boolean).
    """
    height, width = grid.shape
    visited = set()
    objects = []
    
    # First pass: Find connected non-zero components (object pixels)
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and (r, c) not in visited:
                # Found the start of a new non-zero component
                current_object_coords = set()
                current_object_colors = set()
                q = deque([(r, c)])
                visited.add((r, c))
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    current_object_coords.add((row, col))
                    current_object_colors.add(grid[row, col])
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] != 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                if current_object_coords:
                    objects.append({
                        'coords': current_object_coords,
                        'colors': current_object_colors,
                        'has_gray': 5 in current_object_colors,
                        'bounding_box': (min_r, min_c, max_r, max_c),
                        'internal_holes': set() # To be filled later
                    })

    # Second pass: Identify internal holes for each object
    all_object_pixels = set().union(*[obj['coords'] for obj in objects])
    
    # Find all background pixels potentially reachable from the outer border
    reachable_background = set()
    q_background = deque()
    
    # Add all border background pixels to the queue
    for r in range(height):
        if grid[r, 0] == 0 and (r, 0) not in reachable_background:
             q_background.append((r, 0))
             reachable_background.add((r,0))
        if grid[r, width-1] == 0 and (r, width-1) not in reachable_background:
             q_background.append((r, width-1))
             reachable_background.add((r,width-1))
    for c in range(width):
        if grid[0, c] == 0 and (0, c) not in reachable_background:
             q_background.append((0, c))
             reachable_background.add((0,c))
        if grid[height-1, c] == 0 and (height-1, c) not in reachable_background:
             q_background.append((height-1, c))
             reachable_background.add((height-1,c))

    # BFS from border background pixels
    while q_background:
        r, c = q_background.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == 0 and (nr, nc) not in reachable_background:
                reachable_background.add((nr, nc))
                q_background.append((nr, nc))

    # Assign internal holes to objects
    for obj in objects:
        min_r, min_c, max_r, max_c = obj['bounding_box']
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                # If a pixel is background(0), within the bounding box,
                # and NOT reachable from the outer border, it's an internal hole for *some* object.
                # We assume it belongs to the object defining this bounding box for simplicity in this task structure.
                # A more complex check might be needed if objects interleave holes.
                if grid[r,c] == 0 and (r,c) not in reachable_background and (r,c) not in all_object_pixels:
                     # Double check adjacency to *this* object's coords - improves robustness slightly
                     is_adjacent_to_this_obj = False
                     for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                         nr, nc = r + dr, c + dc
                         if (nr, nc) in obj['coords']:
                             is_adjacent_to_this_obj = True
                             break
                     if is_adjacent_to_this_obj:
                         obj['internal_holes'].add((r, c))

    return objects


def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid (np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Define the color transformation maps
    map_gray_present = {
        1: 4,  # Blue -> Yellow
        2: 2,  # Red -> Red
        4: 3,  # Yellow -> Green
        3: 1   # Green -> Blue
    }
    map_gray_absent = {
        4: 6,  # Yellow -> Magenta
        2: 7,  # Red -> Orange
        6: 2,  # Magenta -> Red
        7: 4   # Orange -> Yellow
    }

    # Find all objects and their internal holes in the input grid
    objects = _find_objects(input_grid)

    # Process each object
    for obj in objects:
        coords = obj['coords']
        colors = obj['colors']
        has_gray = obj['has_gray']
        internal_holes = obj['internal_holes']
        
        primary_color = -1
        target_color = -1

        # Determine primary color and apply transformation map
        if has_gray:
            primary_colors = [c for c in colors if c != 0 and c != 5]
            if primary_colors: # Should have exactly one based on examples
                 primary_color = primary_colors[0]
                 target_color = map_gray_present.get(primary_color, primary_color) # Default to itself if not in map
            # else: handle unexpected case like only gray? Keep original color maybe?
            # target_color remains -1 or handle explicitly. For now assume valid primary.
            
        else: # No gray color (5) in the object
            primary_colors = [c for c in colors if c != 0]
            if len(primary_colors) == 1: # Should have exactly one based on examples
                primary_color = primary_colors[0]
                target_color = map_gray_absent.get(primary_color, primary_color) # Default to itself if not in map
            # else: handle unexpected case like multiple non-gray colors? Keep original?
            # target_color remains -1 or handle explicitly. For now assume valid primary.

        # Update the output grid for all pixels belonging to the object's footprint
        if target_color != -1: # Ensure we found a valid transformation target
            all_pixels_to_update = coords.union(internal_holes)
            for r, c in all_pixels_to_update:
                 # Bounds check just in case, though coords should be valid
                if 0 <= r < height and 0 <= c < width:
                    output_grid[r, c] = target_color
        # If target_color remained -1 (due to unexpected object composition),
        # the original colors in output_grid (copied from input) are preserved for that object.

    return output_grid
```
```python
import numpy as np
from collections import deque

"""
Transforms the input grid based on object colors and the presence of gray (5), filling internal holes.

1.  Identifies distinct objects in the input grid. An object consists of:
    *   A core set of connected non-white (non-zero) pixels ('Pixels').
    *   An optional set of enclosed white (0) pixels ('Internal_Holes') surrounded by the object's 'Pixels'.
2.  For each object, checks if gray (5) is present among its core pixels.
3.  Determines a 'primary color':
    *   If gray is present, it's the other non-white color.
    *   If gray is absent, it's the single non-white color.
4.  Applies one of two color transformation rules to the primary color based on gray's presence, yielding a 'target output color':
    *   Rule (Gray Present): Blue(1)->Yellow(4), Red(2)->Red(2), Yellow(4)->Green(3), Green(3)->Blue(1).
    *   Rule (Gray Absent): Yellow(4)->Magenta(6), Red(2)->Orange(7), Magenta(6)->Red(2), Orange(7)->Yellow(4).
5.  Updates the output grid by setting all pixels corresponding to the object's core ('Pixels') and its 'Internal_Holes' to the 'target output color'.
6.  External background pixels remain unchanged.
"""

def _find_objects_and_holes(grid):
    """
    Finds connected components (objects) of non-background pixels 
    and associates enclosed background pixels (internal holes) with them.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'coords' (set of non-zero pixel coordinates),
              'internal_holes' (set of enclosed zero pixel coordinates),
              'colors' (set of non-zero color values), and 'has_gray' (boolean).
    """
    height, width = grid.shape
    visited_objects = set()
    objects = []
    all_object_pixels = set()

    # --- Step 1: Find connected non-zero components (object pixels) ---
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and (r, c) not in visited_objects:
                # Found the start of a new non-zero component
                current_object_coords = set()
                current_object_colors = set()
                q = deque([(r, c)])
                visited_objects.add((r, c))

                while q:
                    row, col = q.popleft()
                    current_object_coords.add((row, col))
                    current_object_colors.add(grid[row, col])
                    all_object_pixels.add((row, col)) # Keep track of all object pixels globally

                    # Check 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] != 0 and (nr, nc) not in visited_objects:
                            visited_objects.add((nr, nc))
                            q.append((nr, nc))
                
                if current_object_coords:
                    objects.append({
                        'coords': current_object_coords,
                        'colors': current_object_colors,
                        'has_gray': 5 in current_object_colors,
                        'internal_holes': set() # Initialize hole set for this object
                    })

    # --- Step 2: Identify all background pixels reachable from the border ---
    reachable_background = set()
    q_background = deque()
    
    # Add all border background pixels to the queue if they are background(0)
    for r in range(height):
        if grid[r, 0] == 0: q_background.append((r, 0)); reachable_background.add((r,0))
        if grid[r, width-1] == 0: q_background.append((r, width-1)); reachable_background.add((r,width-1))
    # Avoid adding corners twice
    for c in range(1, width - 1): 
        if grid[0, c] == 0: q_background.append((0, c)); reachable_background.add((0,c))
        if grid[height-1, c] == 0: q_background.append((height-1, c)); reachable_background.add((height-1,c))

    # BFS from border background pixels to find all connected external background
    visited_background = set(reachable_background) # Use separate visited set for background BFS
    while q_background:
        r, c = q_background.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == 0 and (nr, nc) not in visited_background:
                visited_background.add((nr, nc))
                reachable_background.add((nr, nc))
                q_background.append((nr, nc))

    # --- Step 3: Identify internal holes and associate them with objects ---
    for r in range(height):
        for c in range(width):
            # If a pixel is background(0) and not reachable from the outside, it's an internal hole
            if grid[r, c] == 0 and (r, c) not in reachable_background:
                hole_coord = (r, c)
                # Find which object this hole belongs to by checking adjacent pixels
                adjacent_object_found = False
                for obj in objects:
                     # Check if any neighbor of the hole is part of this object's coordinates
                     is_adjacent = False
                     for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                         nr, nc = r + dr, c + dc
                         if (nr, nc) in obj['coords']:
                             is_adjacent = True
                             break
                     if is_adjacent:
                         obj['internal_holes'].add(hole_coord)
                         adjacent_object_found = True
                         # Assuming a hole belongs to only one object based on problem structure
                         break 
                # Optional: Handle case where a hole isn't adjacent to any identified object? 
                # This shouldn't happen if object finding is correct for ARC tasks.

    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Define the color transformation maps
    map_gray_present = {
        1: 4,  # Blue -> Yellow
        2: 2,  # Red -> Red
        4: 3,  # Yellow -> Green
        3: 1   # Green -> Blue
    }
    map_gray_absent = {
        4: 6,  # Yellow -> Magenta
        2: 7,  # Red -> Orange
        6: 2,  # Magenta -> Red
        7: 4   # Orange -> Yellow
    }

    # Find all objects and their associated internal holes
    objects = _find_objects_and_holes(input_grid)

    # Process each object
    for obj in objects:
        coords = obj['coords']
        colors = obj['colors']
        has_gray = obj['has_gray']
        internal_holes = obj['internal_holes']
        
        primary_color = -1
        target_color = -1

        # Determine primary color based on presence of gray
        if has_gray:
            # Find the non-gray, non-zero color
            primary_colors = [c for c in colors if c != 0 and c != 5]
            if primary_colors: # Should have exactly one based on examples
                 primary_color = primary_colors[0]
                 # Apply the transformation rule for objects with gray
                 target_color = map_gray_present.get(primary_color, primary_color) 
            else:
                 # Handle case of object being *only* gray (not seen in examples)
                 # Default: keep gray as gray? or treat as error? Keeping gray for now.
                 if colors == {5}:
                     target_color = 5 
            
        else: # No gray color (5) in the object
            # Find the single non-zero color
            primary_colors = [c for c in colors if c != 0]
            if len(primary_colors) == 1: # Should have exactly one based on examples
                primary_color = primary_colors[0]
                # Apply the transformation rule for objects without gray
                target_color = map_gray_absent.get(primary_color, primary_color) 
            # else: Handle case of multiple non-gray colors without gray (not seen in examples)
            # Default: Keep original colors by not setting target_color? For now assume valid input.

        # Update the output grid for all pixels in the object's footprint (coords + holes)
        if target_color != -1: # Ensure we found a valid transformation target
            all_pixels_to_update = coords.union(internal_holes)
            for r, c in all_pixels_to_update:
                 # Bounds check just for safety
                if 0 <= r < height and 0 <= c < width:
                    output_grid[r, c] = target_color
        # If target_color remained -1 (due to unexpected object composition),
        # the original colors in output_grid (copied from input) are preserved for that object.

    return output_grid
```
