
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2
0 2 1 2 0 0 2 1 2
0 2 2 2 0 0 2 2 2
0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 8 8 8
0 4 1 4 0 0 8 1 8
0 4 4 4 0 0 8 8 8
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 8 8 8
0 4 1 4 0 0 8 1 8
0 4 4 4 0 0 8 8 8
0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3
0 6 6 6 0 0 3 7 7 7 3
0 6 7 6 0 0 3 7 7 7 3
0 6 6 6 0 0 3 7 7 7 3
0 0 0 0 0 0 3 3 3 3 3
5 5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 3 3 3 3 0 0
5 5 7 5 5 3 7 7 3 0 0
5 5 5 5 5 3 7 7 3 0 0
5 5 5 5 5 3 3 3 3 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0
0 6 7 6 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
5 5 7 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 1 1 1
0 4 0 0 0 4 0 0 0 1 0 1
0 4 4 4 4 4 0 0 0 1 0 1
0 0 0 0 0 4 4 4 0 1 0 1
0 0 0 0 0 4 0 4 0 1 1 1
7 7 7 0 0 4 0 4 0 0 0 0
7 0 7 0 0 4 4 4 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 1 1
7 7 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 0
```

Okay, let's break down the task based on the provided examples.

**Perception of Elements:**

1.  **Background:** The grid uses white (0) as the background color.
2.  **Objects:** The input grids contain multiple distinct objects composed of non-white pixels. These objects are separated by the white background.
3.  **Object Structure:** The objects in the examples often exhibit a structure with an outer "frame" color and one or more "internal" colors.
    *   In `train_1`, objects are 3x3 squares with a frame color (Red, Yellow, or Azure) and a single internal center pixel (Blue).
    *   In `train_2`, some objects are 3x3 squares with a frame (Magenta or Gray) and a center pixel (Orange). Others are rectangles (Green frame) with a more complex internal shape (Orange).
    *   In `train_3`, objects have a frame color (Yellow, Blue, or Orange) and internal pixels of the background color (White).
4.  **Transformation:** The transformation involves selectively removing *entire* objects from the input grid. Removed objects are replaced with the background color (white).
5.  **Selection Criteria:** The key is to determine *which* objects are removed. Observing the examples, the removal seems dependent on the specific combination of the object's frame color and its internal color(s).
    *   `train_1`: Objects with a Red frame and Blue center are removed. Objects with Yellow/Azure frames and Blue centers are kept.
    *   `train_2`: Objects with a Green frame and Orange internal pixels are removed. Objects with Magenta/Gray frames and Orange centers are kept.
    *   `train_3`: Objects with a Yellow frame and White internal pixels are removed. Objects with Blue/Orange frames and White internal pixels are kept.

**YAML Facts:**


```yaml
task_description: Identify specific types of two-colored objects and remove them, keeping all other objects.

definitions:
  background_color: 0 # white
  object: A contiguous group of non-background pixels.

rules:
  - description: Iterate through each distinct object in the input grid.
  - conditions:
      - object_must_have_two_colors: True
      - define_frame_color: The color forming the outer boundary of the object.
      - define_internal_color: The color(s) enclosed by the frame color.
  - removal_criteria:
      - description: Remove the object if its (Internal Color, Frame Color) pair matches a specific set.
      - pairs_to_remove:
          - internal: 1 # blue
            frame: 2 # red
          - internal: 7 # orange
            frame: 3 # green
          - internal: 0 # white
            frame: 4 # yellow
  - action:
      - if: removal_criteria met
        then: Replace all pixels of the object with the background_color.
      - else: Keep the object unchanged.

output_grid: The modified input grid after applying the removal action based on the criteria.

examples:
  train_1:
    objects:
      - { frame: 2, internal: 1, action: remove }
      - { frame: 2, internal: 1, action: remove }
      - { frame: 4, internal: 1, action: keep }
      - { frame: 8, internal: 1, action: keep }
  train_2:
    objects:
      - { frame: 6, internal: 7, action: keep }
      - { frame: 3, internal: 7, action: remove }
      - { frame: 5, internal: 7, action: keep }
      - { frame: 3, internal: 7, action: remove }
  train_3:
    objects:
      - { frame: 4, internal: 0, action: remove }
      - { frame: 1, internal: 0, action: keep }
      - { frame: 7, internal: 0, action: keep }

```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct objects in the input grid. An object is a connected component of pixels with non-zero colors.
3.  For each identified object:
    a.  Determine the set of unique colors present within the object.
    b.  Check if the object consists of exactly two distinct colors (this includes cases where one of the "colors" is the background color 0, provided it is fully enclosed within the object's non-zero pixels).
    c.  If the object has exactly two colors, identify the 'Frame Color' (the color forming the outer boundary) and the 'Internal Color' (the color enclosed by the frame).
    d.  Check if the (Internal Color, Frame Color) pair matches any of the following specific pairs:
        *   (Blue (1), Red (2))
        *   (Orange (7), Green (3))
        *   (White (0), Yellow (4))
    e.  If a match is found in step (d), locate all pixels belonging to this object in the output grid and change their color to the background color (White, 0).
4.  Return the modified output grid. Objects that did not meet the removal criteria remain unchanged from the input.
```python
import collections
import copy

"""
Transformation rule:
Identify distinct objects composed of non-background pixels (color > 0).
For each object, determine all colors involved: the colors of the object's pixels and any background (0) pixels that are fully enclosed within the object's structure (i.e., cannot reach the grid border via other background pixels).
If an object, including its enclosed background pixels, consists of exactly two distinct colors, identify the 'frame' color (the one touching the external background) and the 'internal' color (the one not touching the external background, or the background color 0 if it's enclosed).
Check if the (internal_color, frame_color) pair matches specific removal criteria: (Blue(1), Red(2)), (Orange(7), Green(3)), or (White(0), Yellow(4)).
If a match is found, remove the object by replacing all of its original non-background pixels with the background color (0). Otherwise, keep the object unchanged.
"""


def _get_neighbors(r, c, height, width):
    """Gets valid neighbor coordinates (up, down, left, right)."""
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, c))
    if r < height - 1:
        neighbors.append((r + 1, c))
    if c > 0:
        neighbors.append((r, c - 1))
    if c < width - 1:
        neighbors.append((r, c + 1))
    return neighbors

def _find_objects(grid: list[list[int]]) -> list[set[tuple[int, int]]]:
    """
    Finds connected components of non-background pixels using Breadth-First Search (BFS).
    
    Args:
        grid: The input grid (list of lists of integers).

    Returns:
        A list of sets, where each set contains the (row, col) coordinates
        of the pixels belonging to a distinct object.
    """
    height = len(grid)
    width = len(grid[0])
    visited = set()
    objects = []
    background_color = 0

    for r in range(height):
        for c in range(width):
            # Look for non-background pixels that haven't been visited yet
            if grid[r][c] != background_color and (r, c) not in visited:
                # Found the start of a new object, perform BFS
                obj_coords = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))
                obj_coords.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()
                    # Explore neighbors
                    for nr, nc in _get_neighbors(curr_r, curr_c, height, width):
                        # Add neighbor to object if it's non-background and not visited
                        if (nr, nc) not in visited and grid[nr][nc] != background_color:
                            visited.add((nr, nc))
                            obj_coords.add((nr, nc))
                            q.append((nr, nc))
                # Add the completed object to the list
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def _find_border_background(grid: list[list[int]]) -> set[tuple[int, int]]:
    """
    Finds all background pixels connected to the grid border using BFS.
    This helps identify enclosed background pixels later.

    Args:
        grid: The input grid.

    Returns:
        A set of (row, col) coordinates of background pixels connected to the border.
    """
    height = len(grid)
    width = len(grid[0])
    border_background = set()
    q = collections.deque()
    visited = set()
    background_color = 0

    # Initialize queue with all background pixels on the border
    for r in range(height):
        if grid[r][0] == background_color and (r, 0) not in visited:
            q.append((r, 0))
            visited.add((r, 0))
        # Check width > 1 to avoid index error on 1-wide grids
        if width > 1 and grid[r][width - 1] == background_color and (r, width - 1) not in visited:
            q.append((r, width - 1))
            visited.add((r, width - 1))
    for c in range(width):
        if grid[0][c] == background_color and (0, c) not in visited:
             q.append((0, c))
             visited.add((0, c))
        # Check height > 1 to avoid index error on 1-high grids
        if height > 1 and grid[height - 1][c] == background_color and (height - 1, c) not in visited:
             q.append((height - 1, c))
             visited.add((height - 1, c))
    
    border_background.update(visited) # Add initial border pixels found

    # Perform BFS starting from the border background pixels
    while q:
        curr_r, curr_c = q.popleft()
        for nr, nc in _get_neighbors(curr_r, curr_c, height, width):
            # If neighbor is background and not visited, add it
            if (nr, nc) not in visited and grid[nr][nc] == background_color:
                visited.add((nr, nc))
                border_background.add((nr, nc))
                q.append((nr, nc))

    return border_background


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    Identifies objects composed of exactly two colors (where one might be enclosed background).
    Removes objects if their (internal_color, frame_color) pair matches specific criteria:
    (Blue(1), Red(2)), (Orange(7), Green(3)), or (White(0), Yellow(4)).

    Args:
        input_grid: The input grid represented as a list of lists of integers.

    Returns:
        The transformed grid as a list of lists of integers.
    """
    # Create a deep copy to modify, preserving the original input
    output_grid = copy.deepcopy(input_grid)
    height = len(input_grid)
    width = len(input_grid[0])
    background_color = 0

    # Define the specific pairs (internal_color, frame_color) to be removed
    # (Blue, Red), (Orange, Green), (White, Yellow)
    removal_pairs = {(1, 2), (7, 3), (0, 4)}

    # Find all distinct objects (connected components of non-background colors)
    objects = _find_objects(input_grid)

    # Pre-calculate which background pixels are connected to the border
    # This helps efficiently determine if a background pixel is enclosed
    border_background_coords = _find_border_background(input_grid)

    # Process each identified object
    for obj_coords in objects:
        if not obj_coords: continue # Skip if object is somehow empty

        # 1. Determine colors within the object's non-background pixels
        obj_colors_non_zero = {input_grid[r][c] for r, c in obj_coords}

        # 2. Find the bounding box of the object for efficient enclosed background check
        min_r = min(r for r, c in obj_coords)
        max_r = max(r for r, c in obj_coords)
        min_c = min(c for r, c in obj_coords)
        max_c = max(c for r, c in obj_coords)

        # 3. Check for enclosed background pixels within the bounding box
        # An enclosed background pixel is one with color 0, within the bbox,
        # and not connected to the border background.
        has_enclosed_background = False
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                coord = (r, c)
                # Check if pixel is background and NOT connected to the border background
                if input_grid[r][c] == background_color and coord not in border_background_coords:
                     # Also check if this enclosed background pixel is adjacent to the current object
                     # to ensure it's relevant to *this* object's structure.
                     is_adjacent_to_object = False
                     for nr, nc in _get_neighbors(r, c, height, width):
                         if (nr, nc) in obj_coords:
                             is_adjacent_to_object = True
                             break
                     if is_adjacent_to_object:
                        has_enclosed_background = True
                        break # Found one relevant enclosed background pixel, no need to check further
            if has_enclosed_background:
                break

        # 4. Combine object colors and potentially the enclosed background color (0)
        all_obj_colors = set(obj_colors_non_zero)
        if has_enclosed_background:
            all_obj_colors.add(background_color)

        # 5. Proceed only if the object involves exactly two colors in total
        if len(all_obj_colors) == 2:
            colors = list(all_obj_colors)
            c1, c2 = colors[0], colors[1]

            # 6. Determine which color is the frame (touches external background)
            # External background means pixels outside the object that are connected to the border background.
            c1_touches_external = False
            c2_touches_external = False

            for r, c in obj_coords:
                pixel_color = input_grid[r][c]
                # Check neighbors for external background connection
                for nr, nc in _get_neighbors(r, c, height, width):
                    neighbor_coord = (nr, nc)
                    # Check if neighbor is outside the object's coordinates, is background, and touches the border
                    if neighbor_coord not in obj_coords and input_grid[nr][nc] == background_color and neighbor_coord in border_background_coords:
                        if pixel_color == c1:
                            c1_touches_external = True
                        elif pixel_color == c2:
                            c2_touches_external = True
                        # Optimization: if both touch, we know enough for this pixel check
                        if c1_touches_external and c2_touches_external: break
                # Optimization: if both touch external, no need to check more pixels of the object
                if c1_touches_external and c2_touches_external: break

            # 7. Assign frame and internal based on which color touches the external background
            frame_color = -1 # Sentinel value indicates ambiguity or error
            internal_color = -1

            if c1_touches_external and not c2_touches_external:
                 # c1 touches external, c2 does not -> c1 is frame, c2 is internal
                 frame_color = c1
                 internal_color = c2
            elif c2_touches_external and not c1_touches_external:
                 # c2 touches external, c1 does not -> c2 is frame, c1 is internal
                 frame_color = c2
                 internal_color = c1
            elif not c1_touches_external and not c2_touches_external:
                 # Neither touches external background.
                 # This occurs if the object is fully enclosed by another structure,
                 # or if the only background it touches is itself enclosed background.
                 # If one of the colors is background(0) (meaning it was enclosed), it must be the internal color.
                 if c1 == background_color:
                      internal_color = c1
                      frame_color = c2
                 elif c2 == background_color:
                      internal_color = c2
                      frame_color = c1
                 # else: Both are non-background and don't touch external -> Treat as non-removable based on this rule
            elif c1_touches_external and c2_touches_external:
                 # Both touch external background. Example: adjacent stripes of two colors.
                 # This structure doesn't fit the 'frame/internal' model clearly.
                 # However, if one color is background(0), it must be internal (this case should be unlikely
                 # if background(0) is identified correctly as enclosed, which shouldn't touch external).
                 # If background(0) is one of the colors and it somehow touches external, treat it as internal.
                 if c1 == background_color:
                      internal_color = c1
                      frame_color = c2
                 elif c2 == background_color:
                      internal_color = c2
                      frame_color = c1
                 # else: Both are non-background, both touch external -> Not a frame/internal structure, keep object.

            # 8. Check if the identified (internal, frame) pair is in the removal set
            should_remove = False
            if internal_color != -1 and frame_color != -1: # Check if colors were successfully assigned
                if (internal_color, frame_color) in removal_pairs:
                    should_remove = True

            # 9. If removal criteria met, update the output grid
            # Replace all pixels of the original object (non-zero colors) with the background color
            if should_remove:
                for r_obj, c_obj in obj_coords:
                    output_grid[r_obj][c_obj] = background_color

    return output_grid
```
