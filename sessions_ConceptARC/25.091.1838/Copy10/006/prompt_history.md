
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 2 2 2 2 0 3 0 0 0 0 2 2 2 2 0 0 0 0
0 0 3 0 2 2 2 2 0 3 0 0 0 0 2 2 2 2 0 0 0 0
0 0 3 0 2 2 2 2 0 3 0 0 0 0 2 2 2 2 0 0 0 0
0 0 3 0 2 2 2 2 0 3 0 0 0 0 2 2 2 2 0 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 3 0 0 3 0 0 0 0 0 0 3 0 0
0 0 3 0 2 2 2 2 0 3 0 0 3 0 2 2 2 2 0 3 0 0
0 0 3 0 2 2 2 2 0 3 0 0 3 0 2 2 2 2 0 3 0 0
0 0 3 0 2 2 2 2 0 3 0 0 3 0 2 2 2 2 0 3 0 0
0 0 3 0 2 2 2 2 0 3 0 0 3 0 2 2 2 2 0 3 0 0
0 0 3 0 0 0 0 0 0 3 0 0 3 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 0 0 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0
0 0 0 4 0 0 0
0 0 4 0 4 0 0
0 4 0 1 0 4 0
4 0 1 1 1 0 4
0 4 0 1 0 4 0
0 0 4 0 4 0 0
0 0 0 4 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 1 0 0 0
0 0 1 1 1 0 0
0 0 0 1 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 0 0 4 0 0 0
0 0 4 0 4 0 0
0 4 0 1 0 4 0
4 0 1 1 1 0 4
0 4 0 1 0 4 0
0 0 4 0 4 0 0
0 0 0 4 0 0 0
0 0 0 0 0 0 0
0 0 0 4 0 0 0
0 0 4 0 4 0 0
0 4 0 1 0 4 0
4 0 1 1 1 0 4
0 4 0 1 0 4 0
0 0 4 0 4 0 0
0 0 0 4 0 0 0
0 0 0 0 0 0 0
```

Okay, let's break down the task based on the provided examples.

**Perception**

1.  **Input Structure:** The input grids contain multiple distinct geometric shapes (objects) composed of colored pixels against a white background.
2.  **Object Relationships:** In both examples, there's a primary larger object ("container") that encloses one or more smaller objects within its spatial boundary (bounding box). There is also at least one other object ("orphan") located elsewhere in the grid, separate from the container and its contents.
3.  **Transformation:** The core transformation involves identifying the container and its enclosed objects, identifying the separate orphan object, removing the orphan object, and then creating a duplicate of the container and its contents.
4.  **Placement of Copy:** The duplicated container+contents structure is placed in the grid in a location determined by the original position of the orphan object. Specifically, the copy seems to be positioned such that its bounding box edge (the one facing the original container) is 2 pixels away from the corresponding edge of the *original* orphan object's bounding box.
5.  **Overwriting:** The copied structure overwrites any pixels previously occupying that space, including the area where the orphan object was removed. The original container and its contents remain unchanged in their initial position.

**Facts**


```yaml
task_description: Copy a 'container' object and its 'contained' objects to a new location determined by an 'orphan' object, replacing the orphan object.

definitions:
  - object: A contiguous block of non-white pixels.
  - bounding_box: The smallest rectangle enclosing all pixels of an object.
  - container: An object whose bounding box fully encloses the bounding box(es) of one or more other objects. (In these examples, it's the object enclosing the most others).
  - contained_object: An object whose bounding box is fully within the bounding box of the container.
  - orphan_object: An object that is neither the container nor a contained object. (Assume one primary orphan determines placement).

steps:
  - step: 1
    action: identify_objects
    description: Find all distinct objects (contiguous non-white pixels) and their bounding boxes in the input grid.
  - step: 2
    action: identify_container
    description: Determine which object is the container by finding the object whose bounding box encloses the most other objects' bounding boxes.
  - step: 3
    action: identify_contained
    description: Identify all objects whose bounding boxes are fully within the container's bounding box.
  - step: 4
    action: identify_orphan
    description: Identify the object(s) that are neither the container nor contained. Assume a single primary orphan dictates placement.
  - step: 5
    action: calculate_copy_location
    inputs:
      - container_bounding_box
      - orphan_bounding_box
    description: >
      Determine the top-left coordinates (target_row, target_col) for placing the copy of the container.
      Find the axis of greatest separation between the container and orphan bounding boxes.
      If horizontal separation (orphan is right of container):
        target_row = container.top
        target_col = orphan.left - 2
      If vertical separation (orphan is below container):
        target_row = orphan.top - 2
        target_col = container.left
      (Adjust logic if orphan is left/above container, though not seen in examples).
  - step: 6
    action: prepare_output_grid
    inputs:
      - input_grid
      - orphan_object
    description: Create a copy of the input grid. Set all pixels belonging to the orphan object to white (0).
  - step: 7
    action: extract_pattern_to_copy
    inputs:
      - input_grid
      - container_bounding_box
    description: Extract the subgrid defined by the container's bounding box from the original input grid (this includes the container and all contained objects).
  - step: 8
    action: place_copy
    inputs:
      - output_grid
      - pattern_to_copy
      - target_location (target_row, target_col)
    description: Paste the extracted subgrid (pattern_to_copy) onto the output grid starting at the calculated target location, overwriting existing pixels.

final_output: The modified output grid after removing the orphan and placing the copy.
```


**Natural Language Program**

1.  Analyze the input grid to identify all separate objects (groups of connected, non-white pixels) and determine their bounding boxes.
2.  Identify the "container" object, defined as the object whose bounding box encloses the highest number of other objects.
3.  Identify all "contained" objects, whose bounding boxes lie entirely inside the container's bounding box.
4.  Identify the "orphan" object(s), which are neither the container nor contained within it. (Assume there's one primary orphan used for positioning).
5.  Determine the placement coordinates for a copy of the container. Find the orphan's bounding box. Calculate the target top-left corner for the container copy by finding the main axis separating the container and the orphan, and positioning the copy's corresponding edge 2 pixels away from the orphan's corresponding edge, towards the original container's side. Maintain the other coordinate (row or column) from the original container's top-left position.
6.  Create the output grid by first copying the input grid.
7.  Remove the orphan object from the output grid by changing its pixels to white (0).
8.  Copy the rectangular region defined by the container's bounding box from the *original input grid* (this includes the container and all its contained objects).
9.  Paste this copied region onto the output grid at the calculated placement coordinates, overwriting any existing pixels.
10. The resulting grid is the final output.
```python
import numpy as np
from collections import deque

"""
This module transforms an input grid based on identifying container, contained, and orphan objects.
The transformation involves:
1. Identifying all distinct objects (contiguous blocks of non-white pixels) and their bounding boxes.
2. Finding the 'container' object, defined as the object whose bounding box encloses the most other objects.
3. Identifying 'contained' objects lying fully within the container's bounding box.
4. Identifying 'orphan' objects, which are neither the container nor contained. (Assuming one primary orphan determines placement).
5. Calculating a target location for a copy of the container and its contents. This location is determined by the position of the primary orphan object, placing the copy's edge 2 pixels away from the orphan's corresponding edge, towards the original container.
6. Creating an output grid by copying the input grid.
7. Removing the orphan object from the output grid (setting its pixels to white).
8. Extracting the rectangular region defined by the container's bounding box from the original input grid.
9. Pasting this extracted region onto the output grid at the calculated target location, overwriting existing pixels.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of tuples, where each tuple represents an object and contains:
              - set: A set of (row, col) coordinates of the object's pixels.
              - tuple: The bounding box (min_r, min_c, max_r, max_c).
              - int: The color of the object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-directional)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if obj_coords:
                    bounding_box = (min_r, min_c, max_r, max_c)
                    objects.append((obj_coords, bounding_box, color))
    return objects

def is_enclosed(inner_box, outer_box):
    """Checks if inner_box is strictly inside outer_box."""
    min_r1, min_c1, max_r1, max_c1 = inner_box
    min_r2, min_c2, max_r2, max_c2 = outer_box
    return min_r1 > min_r2 and min_c1 > min_c2 and max_r1 < max_r2 and max_c1 < max_c2

def transform(input_grid):
    """
    Transforms the input grid by copying a container object based on an orphan object's position.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    output_np = np.copy(input_np)

    # 1. Identify all objects
    all_objects = find_objects(input_np)
    if not all_objects:
        return input_grid # Return original if no objects

    # 2. Identify the container
    container = None
    container_box = None
    container_coords = None
    max_enclosed_count = -1

    for i, (coords_i, box_i, color_i) in enumerate(all_objects):
        enclosed_count = 0
        for j, (coords_j, box_j, color_j) in enumerate(all_objects):
            if i == j:
                continue
            if is_enclosed(box_j, box_i):
                enclosed_count += 1
        
        # Prioritize larger containers if counts are equal
        current_area = (box_i[2] - box_i[0] + 1) * (box_i[3] - box_i[1] + 1)
        if enclosed_count > max_enclosed_count:
            max_enclosed_count = enclosed_count
            container = all_objects[i]
        elif enclosed_count == max_enclosed_count and container:
             # If counts are equal, choose the one with larger bounding box area
             prev_box = container[1]
             prev_area = (prev_box[2] - prev_box[0] + 1) * (prev_box[3] - prev_box[1] + 1)
             if current_area > prev_area:
                 container = all_objects[i]


    if container is None:
         # Handle cases where no container is found (e.g., only one object)
         # Based on examples, this shouldn't happen, but good to consider.
         # Maybe default to the largest object if no enclosure?
         if all_objects:
             container = max(all_objects, key=lambda obj: len(obj[0])) # Largest by pixel count as fallback
         else:
             return input_grid # Still no objects


    container_coords, container_box, _ = container
    c_min_r, c_min_c, c_max_r, c_max_c = container_box


    # 3. Identify contained objects (needed to identify orphans)
    contained_indices = set()
    for i, (coords_i, box_i, color_i) in enumerate(all_objects):
         if i != all_objects.index(container) and is_enclosed(box_i, container_box):
             contained_indices.add(i)

    # 4. Identify the orphan object(s)
    orphan = None
    orphan_box = None
    orphan_coords = None
    # Assume the first object found that isn't container or contained is the primary orphan
    for i, (coords_i, box_i, color_i) in enumerate(all_objects):
         if i != all_objects.index(container) and i not in contained_indices:
              orphan = all_objects[i]
              orphan_coords, orphan_box, _ = orphan
              break # Use the first one found

    if orphan is None:
        # Should not happen based on examples, implies only container + contained exist
        return input_grid 

    o_min_r, o_min_c, o_max_r, o_max_c = orphan_box

    # 5. Calculate copy location
    target_row, target_col = -1, -1
    
    # Determine primary axis of separation (simple check based on bounding box corners)
    is_vertically_separated = o_min_r > c_max_r or o_max_r < c_min_r
    is_horizontally_separated = o_min_c > c_max_c or o_max_c < c_min_c

    if is_vertically_separated and o_min_r > c_max_r: # Orphan below
        target_row = o_min_r - 2
        target_col = c_min_c
    elif is_horizontally_separated and o_min_c > c_max_c: # Orphan right
        target_row = c_min_r
        target_col = o_min_c - 2
    # Add cases for orphan above or left if needed, based on future examples
    # elif is_vertically_separated and o_max_r < c_min_r: # Orphan above
    #     target_row = o_max_r + 2 + 1 # Placeholder, needs validation
    #     target_col = c_min_c
    # elif is_horizontally_separated and o_max_c < c_min_c: # Orphan left
    #     target_row = c_min_r
    #     target_col = o_max_c + 2 + 1 # Placeholder, needs validation
    else:
         # Fallback or error - perhaps they overlap or touch in unexpected ways
         # Or maybe use center points as initially considered
         # For now, rely on clear separation from examples
         print("Warning: Ambiguous or unhandled relative position between container and orphan.")
         return input_grid # Return original if placement unclear


    # 6. Prepare output grid (remove orphan)
    for r, c in orphan_coords:
        if 0 <= r < rows and 0 <= c < cols:
            output_np[r, c] = 0

    # 7. Extract pattern to copy (container + contents from ORIGINAL grid)
    pattern = input_np[c_min_r : c_max_r + 1, c_min_c : c_max_c + 1]
    pattern_h, pattern_w = pattern.shape

    # 8. Place copy
    # Ensure target indices are valid and placement doesn't go out of bounds
    if target_row >= 0 and target_col >= 0:
        end_row = target_row + pattern_h
        end_col = target_col + pattern_w
        # Check bounds before placing
        if end_row <= rows and end_col <= cols:
             output_np[target_row : end_row, target_col : end_col] = pattern
        else:
             # Handle partial placement or clipping if necessary, though examples fit
             print(f"Warning: Calculated copy placement ({target_row},{target_col}) to ({end_row-1},{end_col-1}) might exceed grid bounds ({rows},{cols}). Clipping.")
             # Calculate the slice dimensions for both output grid and pattern
             place_rows = min(pattern_h, rows - target_row)
             place_cols = min(pattern_w, cols - target_col)
             if place_rows > 0 and place_cols > 0:
                 output_np[target_row : target_row + place_rows, target_col : target_col + place_cols] = pattern[:place_rows, :place_cols]

    return output_np.tolist()
```
```python
import numpy as np
from collections import deque
import itertools

"""
Transforms an input grid based on identifying container, contained, and orphan object groups.
The transformation involves:
1. Identifying all distinct objects (contiguous blocks of non-white pixels).
2. Grouping objects by color and determining the combined bounding box for each group.
3. Identifying the 'container group' as the color group whose combined bounding box inclusively encloses the combined bounding box of at least one other color group.
4. Identifying 'contained objects' as individual objects of different colors whose bounding boxes are inclusively enclosed within the container group's bounding box. (Implicitly done by finding enclosed groups).
5. Identifying the 'orphan group' as the color group that is neither the container nor belongs to a group enclosed by the container.
6. Calculating a target location for copying the container structure (the area defined by the container group's bounding box, including contained objects). This location is determined by the relative position of the orphan group's bounding box, leaving a 2-pixel gap between the orphan's original edge and the copy's corresponding edge.
7. Creating an output grid by copying the input grid.
8. Removing all objects belonging to the orphan group from the output grid.
9. Extracting the rectangular region corresponding to the container group's bounding box from the original input grid.
10. Pasting this extracted region onto the output grid at the calculated target location, overwriting existing pixels.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same color in the grid using Breadth-First Search.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dicts, where each dict represents an object and contains:
              - 'id': A unique integer identifier for the object.
              - 'coords': set of (row, col) coordinates.
              - 'bbox': tuple (min_r, min_c, max_r, max_c).
              - 'color': int color value.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    object_id_counter = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-directional: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if obj_coords:
                    bounding_box = (min_r, min_c, max_r, max_c)
                    objects.append({'id': object_id_counter, 'coords': obj_coords, 'bbox': bounding_box, 'color': color})
                    object_id_counter += 1
    return objects

def get_color_groups(objects):
    """
    Groups objects by color and calculates the combined bounding box and coordinates for each group.

    Args:
        objects (list): A list of object dictionaries from find_objects.

    Returns:
        dict: A dictionary where keys are colors and values are dicts containing:
              - 'objects': list of object dicts of that color.
              - 'bbox': tuple (min_r, min_c, max_r, max_c) for the whole group.
              - 'coords': set of all (row, col) coordinates for the group.
    """
    groups = {}
    # Sort colors to ensure deterministic behavior if multiple groups could be container/orphan
    colors = sorted(list(set(obj['color'] for obj in objects)))

    for color in colors:
        color_objects = [obj for obj in objects if obj['color'] == color]
        if not color_objects:
            continue

        # Combine coordinates from all objects of the same color
        all_coords = set().union(*[obj['coords'] for obj in color_objects])
        if not all_coords:
             continue # Should not happen if color_objects is not empty

        # Calculate the combined bounding box for the group
        min_r = min(r for r, c in all_coords)
        min_c = min(c for r, c in all_coords)
        max_r = max(r for r, c in all_coords)
        max_c = max(c for r, c in all_coords)
        combined_bbox = (min_r, min_c, max_r, max_c)

        groups[color] = {
            'objects': color_objects,
            'bbox': combined_bbox,
            'coords': all_coords
        }
    return groups

def is_enclosed(inner_box, outer_box):
    """
    Checks if inner_box is inclusively inside outer_box (edges can touch).
    An object/group cannot enclose itself.

    Args:
        inner_box (tuple): Bbox (min_r, min_c, max_r, max_c).
        outer_box (tuple): Bbox (min_r, min_c, max_r, max_c).

    Returns:
        bool: True if inner_box is enclosed by outer_box, False otherwise.
    """
    min_r1, min_c1, max_r1, max_c1 = inner_box
    min_r2, min_c2, max_r2, max_c2 = outer_box
    # Prevent self-enclosure if boxes are identical
    if inner_box == outer_box:
        return False
    return min_r1 >= min_r2 and min_c1 >= min_c2 and max_r1 <= max_r2 and max_c1 <= max_c2

def transform(input_grid):
    """
    Applies the transformation logic to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    output_np = np.copy(input_np) # Start with a copy of the input

    # Step 1: Find all distinct objects
    all_objects = find_objects(input_np)
    if not all_objects:
        return input_grid # Return original if no objects found

    # Step 2: Group objects by color
    color_groups = get_color_groups(all_objects)
    group_colors = list(color_groups.keys())
    if len(group_colors) < 2: # Need at least a container and something else
        return input_grid

    # Step 3: Identify the Container Group
    container_group_color = -1
    container_group_bbox = None
    enclosed_group_colors = set() # Track colors of groups enclosed by the container

    # Iterate through all pairs of distinct color groups
    for color1, color2 in itertools.permutations(group_colors, 2):
        group1 = color_groups[color1]
        group2 = color_groups[color2]
        # Check if group1's combined bounding box encloses group2's combined bounding box
        if is_enclosed(group2['bbox'], group1['bbox']):
            # Found a potential container (group1) and an enclosed group (group2)
            # Simple strategy: assign the first group found that encloses another.
            # More complex scenarios might need tie-breaking (e.g., largest area).
            if container_group_color == -1:
                 container_group_color = color1
                 container_group_bbox = group1['bbox']
            # Regardless if it's the chosen container, mark group2 as enclosed by *some* group
            enclosed_group_colors.add(color2)

    # If no group encloses another group, the task definition might not apply
    if container_group_color == -1:
         # print("Warning: Could not identify a container group based on enclosing other groups.")
         return input_grid

    # Step 4: (Implicit) Contained objects are within the enclosed groups.

    # Step 5: Identify the Orphan Group
    orphan_group_color = -1
    orphan_group_bbox = None
    orphan_coords = set()

    # An orphan group is one that is NOT the container AND is NOT enclosed by the container
    for color in group_colors:
        if color != container_group_color and color not in enclosed_group_colors:
            # Found an orphan group. Assume the first one dictates placement.
            if orphan_group_color == -1:
                orphan_group_color = color
                orphan_group = color_groups[color]
                orphan_group_bbox = orphan_group['bbox']
                orphan_coords = orphan_group['coords']
                break # Use the first orphan group found

    # If no orphan group is found, the task definition might not apply
    if orphan_group_color == -1:
        # print("Warning: Could not identify an orphan group.")
        return input_grid

    # Step 6: Calculate copy location based on relative positions
    c_min_r, c_min_c, c_max_r, c_max_c = container_group_bbox
    o_min_r, o_min_c, o_max_r, o_max_c = orphan_group_bbox
    target_row, target_col = -1, -1

    # Calculate separation distance (positive if orphan is right/below)
    # A gap of 1 means adjacent bounding boxes. Gap of 0 means touching.
    vert_gap = o_min_r - c_max_r - 1
    horz_gap = o_min_c - c_max_c - 1

    # Determine primary direction based on which side the orphan is on
    # Assume non-overlapping, non-diagonal placement for simplicity based on examples
    is_below = vert_gap >= 0 and o_min_c <= c_max_c and o_max_c >= c_min_c # Check for vertical overlap
    is_right = horz_gap >= 0 and o_min_r <= c_max_r and o_max_r >= c_min_r # Check for horizontal overlap

    # Placement logic requires a 2-pixel gap between orphan edge and copy edge
    if is_below: # Orphan is primarily below container
         target_row = o_min_r - 2 # Place top edge 2 pixels above orphan's top edge
         target_col = c_min_c     # Align left edge with container's left edge
    elif is_right: # Orphan is primarily right of container
         target_row = c_min_r     # Align top edge with container's top edge
         target_col = o_min_c - 2 # Place left edge 2 pixels left of orphan's left edge
    # Add cases for orphan above or left if needed by future examples
    # elif is_above: target_row = o_max_r + 2; target_col = c_min_c
    # elif is_left: target_row = c_min_r; target_col = o_max_c + 2
    else:
        # If relative position is ambiguous (diagonal, overlapping, etc.) or doesn't fit rules
        # print(f"Warning: Ambiguous relative position between container {container_group_bbox} and orphan {orphan_group_bbox}.")
        return input_grid # Cannot determine placement

    # Step 7: Prepare output grid - Remove orphan objects
    for r, c in orphan_coords:
        if 0 <= r < rows and 0 <= c < cols:
            output_np[r, c] = 0 # Set orphan pixels to background color

    # Step 8: Extract pattern to copy from the ORIGINAL input grid
    # The pattern is the rectangular area defined by the container group's bounding box
    pattern = input_np[c_min_r : c_max_r + 1, c_min_c : c_max_c + 1]
    pattern_h, pattern_w = pattern.shape

    # Step 9: Place the copied pattern onto the output grid
    if target_row >= 0 and target_col >= 0 and pattern_h > 0 and pattern_w > 0:
        # Define the target slice in the output grid
        end_row = target_row + pattern_h
        end_col = target_col + pattern_w

        # Calculate clipping boundaries
        paste_start_row = max(0, target_row)
        paste_start_col = max(0, target_col)
        paste_end_row = min(rows, end_row)
        paste_end_col = min(cols, end_col)

        # Calculate corresponding slice from the pattern
        pattern_start_row = max(0, -target_row)
        pattern_start_col = max(0, -target_col)
        pattern_end_row = pattern_start_row + (paste_end_row - paste_start_row)
        pattern_end_col = pattern_start_col + (paste_end_col - paste_start_col)

        # Paste if the calculated slices are valid
        if paste_start_row < paste_end_row and paste_start_col < paste_end_col:
            output_np[paste_start_row:paste_end_row, paste_start_col:paste_end_col] = \
                pattern[pattern_start_row:pattern_end_row, pattern_start_col:pattern_end_col]
        # else:
             # print(f"Warning: Calculated placement ({target_row},{target_col}) resulted in no valid area to paste.")

    # else:
        # print("Warning: Invalid target coordinates or pattern dimensions.")


    # Step 10: Return the modified grid as a list of lists
    return output_np.tolist()
```
```python
import numpy as np
from collections import deque
import itertools

"""
Transforms an input grid by duplicating a composite structure (a 'container' object 
and the 'contained' objects within its bounding box) to a new location. The new 
location is determined by the position of an 'orphan' object, typically one that 
shares characteristics (like color) with a contained object. The process involves:
1. Identifying all distinct objects (contiguous non-white pixels).
2. Identifying the 'container' object, defined as an object whose bounding box 
   inclusively encloses the bounding box of at least one other object of a 
   different color.
3. Identifying 'contained' objects enclosed within the container's bounding box.
4. Identifying 'orphan' objects (neither container nor contained).
5. Selecting a 'primary orphan' (often matching a contained object's color) to 
   dictate placement.
6. Calculating the target location for the copy, maintaining a 2-pixel gap from 
   the primary orphan's original position.
7. Creating an output grid by copying the input.
8. Removing all orphan objects from the output grid.
9. Extracting the pattern (container's bounding box region) from the original input.
10. Pasting the pattern onto the output grid at the target location.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same color in the grid using Breadth-First Search.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dicts, where each dict represents an object and contains:
              - 'id': A unique integer identifier for the object.
              - 'coords': set of (row, col) coordinates.
              - 'bbox': tuple (min_r, min_c, max_r, max_c).
              - 'color': int color value.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    object_id_counter = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c, max_r, max_c = r, c, r, c

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    min_r, min_c, max_r, max_c = min(min_r, row), min(min_c, col), max(max_r, row), max(max_c, col)

                    # Check neighbors (4-directional: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if obj_coords:
                    bounding_box = (min_r, min_c, max_r, max_c)
                    objects.append({'id': object_id_counter, 'coords': obj_coords, 'bbox': bounding_box, 'color': color})
                    object_id_counter += 1
    return objects

def is_inclusively_enclosed(inner_box, outer_box):
    """
    Checks if inner_box is inclusively inside outer_box (edges can touch).
    Requires the boxes to be distinct.

    Args:
        inner_box (tuple): Bbox (min_r, min_c, max_r, max_c).
        outer_box (tuple): Bbox (min_r, min_c, max_r, max_c).

    Returns:
        bool: True if inner_box is enclosed by outer_box, False otherwise.
    """
    if inner_box == outer_box: # An object cannot enclose itself
        return False
    min_r1, min_c1, max_r1, max_c1 = inner_box
    min_r2, min_c2, max_r2, max_c2 = outer_box
    return min_r1 >= min_r2 and min_c1 >= min_c2 and max_r1 <= max_r2 and max_c1 <= max_c2

def transform(input_grid):
    """
    Applies the transformation logic to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Identify all distinct objects
    all_objects = find_objects(input_np)
    if not all_objects:
        return input_grid # Return original if no objects

    # 2. & 3. Identify Container and Contained Objects
    container = None
    contained_objects_map = {} # Store {container_id: [contained_obj1, contained_obj2,...]}

    for obj_i in all_objects:
        current_contained = []
        for obj_j in all_objects:
            if obj_i['id'] == obj_j['id']:
                continue
            # Check for enclosure and different color
            if obj_i['color'] != obj_j['color'] and is_inclusively_enclosed(obj_j['bbox'], obj_i['bbox']):
                 current_contained.append(obj_j)

        if current_contained: # If obj_i encloses at least one object of a different color
             contained_objects_map[obj_i['id']] = current_contained
             # Simple selection: Assume the first object found that meets the criteria is the container
             # More robust logic might be needed for complex cases (e.g., largest area, most enclosed)
             if container is None:
                 container = obj_i

    # If no container identified based on criteria, return original
    if container is None:
        # print("Warning: No container found meeting criteria.")
        return input_grid

    container_id = container['id']
    container_bbox = container['bbox']
    contained_objects = contained_objects_map.get(container_id, [])
    contained_ids = {obj['id'] for obj in contained_objects}
    contained_colors = {obj['color'] for obj in contained_objects}

    # 4. Identify Orphan Objects
    orphan_objects = []
    for obj in all_objects:
        if obj['id'] != container_id and obj['id'] not in contained_ids:
            orphan_objects.append(obj)

    if not orphan_objects:
        # print("Warning: Container and contained objects found, but no orphans.")
        return input_grid # Needs an orphan to determine placement

    # 5. Select Primary Orphan
    primary_orphan = None
    # Look for an orphan whose color matches a contained object's color
    for orphan in orphan_objects:
        if orphan['color'] in contained_colors:
            primary_orphan = orphan
            break # Use the first one found

    # Fallback: If no orphan matches contained color, use the first orphan found
    if primary_orphan is None:
        primary_orphan = orphan_objects[0]
        
    orphan_bbox = primary_orphan['bbox']

    # 6. Calculate Target Location
    c_min_r, c_min_c, c_max_r, c_max_c = container_bbox
    o_min_r, o_min_c, o_max_r, o_max_c = orphan_bbox
    target_row, target_col = -1, -1

    # Determine relative position and calculate target coordinate with 2-pixel gap
    # Check primary directions based on non-overlapping bounding boxes
    is_below = o_min_r > c_max_r
    is_right = o_min_c > c_max_c
    is_above = o_max_r < c_min_r
    is_left = o_max_c < c_min_c

    if is_below:
        target_row = o_min_r - 2
        target_col = c_min_c
    elif is_right:
        target_row = c_min_r
        target_col = o_min_c - 2
    elif is_above: # Added for completeness, untested by examples
        target_row = o_max_r + 2 # Place top edge 2 pixels below orphan's bottom edge
        target_col = c_min_c
    elif is_left: # Added for completeness, untested by examples
        target_row = c_min_r
        target_col = o_max_c + 2 # Place left edge 2 pixels right of orphan's right edge
    else:
        # Handle ambiguous cases if necessary (e.g., diagonal, overlapping)
        # print(f"Warning: Ambiguous relative position between container {container_bbox} and primary orphan {orphan_bbox}.")
        return input_grid # Cannot determine placement

    # 7. Create Output Grid
    output_np = np.copy(input_np)

    # 8. Remove ALL Orphan Objects
    for orphan in orphan_objects:
        for r, c in orphan['coords']:
            if 0 <= r < rows and 0 <= c < cols:
                output_np[r, c] = 0 # Set orphan pixels to background color

    # 9. Extract Pattern from ORIGINAL Input Grid
    pattern = input_np[c_min_r : c_max_r + 1, c_min_c : c_max_c + 1]
    pattern_h, pattern_w = pattern.shape

    # 10. Place Pattern onto Output Grid (with clipping)
    if target_row != -1 and target_col != -1 and pattern_h > 0 and pattern_w > 0:
        # Define the target slice in the output grid
        end_row = target_row + pattern_h
        end_col = target_col + pattern_w

        # Calculate clipping boundaries for pasting
        paste_start_row = max(0, target_row)
        paste_start_col = max(0, target_col)
        paste_end_row = min(rows, end_row)
        paste_end_col = min(cols, end_col)

        # Calculate corresponding slice from the pattern to copy
        pattern_start_row = max(0, -target_row)
        pattern_start_col = max(0, -target_col)
        pattern_end_row = pattern_start_row + (paste_end_row - paste_start_row)
        pattern_end_col = pattern_start_col + (paste_end_col - paste_start_col)

        # Paste if the calculated slices are valid (have positive dimensions)
        if paste_start_row < paste_end_row and paste_start_col < paste_end_col:
            output_np[paste_start_row:paste_end_row, paste_start_col:paste_end_col] = \
                pattern[pattern_start_row:pattern_end_row, pattern_start_col:pattern_end_col]
        # else: # Debugging: uncomment if needed
            # print(f"Warning: Calculated placement ({target_row},{target_col}) resulted in no valid area to paste.")
            # print(f"Paste Area: ({paste_start_row}:{paste_end_row}, {paste_start_col}:{paste_end_col})")
            # print(f"Pattern Area: ({pattern_start_row}:{pattern_end_row}, {pattern_start_col}:{pattern_end_col})")

    # else: # Debugging: uncomment if needed
        # print("Warning: Invalid target coordinates or pattern dimensions for pasting.")
        # print(f"Target: ({target_row},{target_col}), Pattern Shape: ({pattern_h},{pattern_w})")

    # Convert back to list of lists for ARC standard
    return output_np.tolist()
```
