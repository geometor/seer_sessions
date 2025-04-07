
## train_1

**input:**
```
1 2 3 4 1 1 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2
4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1
3 4 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 3 1 4 4 4 4 4 4 4 4 1 2 3 4 1 2 3 4 1 2 3 4 1 1 3 4 1 1 3
1 2 1 4 1 0 0 0 0 4 3 4 1 2 3 4 1 2 3 4 4 4 4 4 4 4 3 4 1 2
4 1 1 4 6 1 1 1 6 4 2 3 4 1 2 3 4 1 2 4 1 0 0 0 0 4 2 3 1 1
3 4 1 4 0 0 0 0 1 4 1 2 3 4 1 2 3 4 1 4 6 0 0 0 6 4 1 2 1 4
1 3 1 4 0 0 0 0 1 4 4 1 2 3 1 1 2 3 1 4 0 0 0 0 0 4 4 1 1 3
1 2 1 4 0 0 0 0 1 4 3 4 1 2 3 4 1 2 3 4 0 0 0 0 0 4 3 4 1 2
4 1 1 4 4 4 4 4 4 4 2 1 4 1 2 3 4 1 2 4 0 0 0 0 1 4 2 3 1 1
3 4 1 2 3 4 1 2 3 4 1 1 3 4 1 2 3 4 1 4 4 4 4 4 4 4 1 2 1 4
1 3 1 1 2 3 4 1 2 3 4 1 1 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 1 3
1 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1
3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 1 4 1 2 3 4 1 1 1 4 1 2 3 4
2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 1 4 1 2 1 4 1 1 3
1 2 3 4 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 2 3 4 1 2
4 1 2 3 4 2 2 3 4 1 2 3 4 1 2 3 4 4 4 4 4 4 4 2 4 1 2 3 4 1
3 4 1 2 3 2 4 4 4 4 4 4 4 4 1 2 4 0 0 0 0 0 4 2 3 4 1 2 3 4
2 3 4 1 2 2 4 0 0 0 0 0 4 3 4 1 4 0 0 0 0 0 4 2 2 1 4 1 2 3
1 2 3 4 1 2 4 6 0 0 0 2 4 2 3 4 4 0 0 0 0 0 4 2 1 2 3 4 1 2
4 1 2 3 4 2 4 0 0 0 0 0 4 1 2 3 4 0 0 0 0 0 4 2 4 1 2 3 4 1
3 4 1 2 3 2 4 0 0 0 0 0 4 1 1 2 4 0 0 0 0 0 4 2 3 4 1 2 3 4
2 3 4 1 2 2 4 2 0 0 0 0 4 3 4 1 4 4 4 4 4 4 4 2 2 3 4 1 2 3
1 2 3 1 1 2 4 4 4 4 4 4 4 2 3 4 1 2 3 4 1 2 3 2 1 2 3 4 1 2
4 1 2 3 4 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 2 3 4 1
3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 1 3 4 1 2 3 4 1 2 3 4 1 2 3 4
2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 1 4 1 2 3 4 1 2 3
1 2 3 4 1 2 3 1 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2
4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1
```


**output:**
```
0 0 0 0 0
6 2 2 2 2
2 0 0 0 0
2 0 0 0 0
2 0 0 0 0
```


## train_2

**input:**
```
4 1 2 3 0 4 4 4 4 4 4 4 4 4 4 3 0 1 2 4 4 1 2 3 4 1 2 4 0 1
1 2 4 0 1 4 3 0 1 2 3 4 1 2 4 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2
2 3 0 1 2 4 0 8 8 8 8 8 8 3 4 1 2 3 0 4 2 3 0 1 4 3 0 1 2 3
3 0 1 2 3 4 1 8 0 4 0 0 8 0 4 2 3 0 1 2 3 0 1 2 3 4 1 2 3 0
0 1 2 3 0 4 2 8 4 4 0 0 8 1 4 3 0 1 2 3 4 4 2 3 0 1 2 3 0 1
1 2 3 0 4 4 4 8 0 4 4 4 8 2 4 0 1 2 3 4 1 2 3 0 1 2 3 0 1 2
2 3 0 1 2 4 0 8 0 4 0 0 8 3 4 1 2 3 4 2 2 2 2 2 2 2 2 2 2 3
3 0 1 2 3 4 1 8 8 8 8 8 8 4 4 2 3 0 1 2 2 2 2 2 2 2 2 2 2 0
0 1 2 3 0 4 2 3 0 1 2 3 0 1 4 3 0 1 2 2 0 1 2 3 0 1 2 3 2 1
1 2 3 0 4 4 4 0 1 2 3 0 1 2 4 0 4 2 3 2 1 8 8 8 8 8 8 0 2 2
2 4 0 1 4 4 0 4 2 3 0 1 2 4 4 1 2 3 0 2 2 8 0 0 0 0 8 1 2 3
3 0 1 2 3 4 1 2 3 0 4 2 3 0 4 4 3 0 1 2 4 8 0 0 0 0 8 2 2 0
4 1 2 3 0 4 2 3 0 1 2 3 4 1 4 4 0 1 2 2 0 8 0 0 0 0 8 3 2 1
1 2 3 0 1 4 3 0 1 2 3 0 1 2 4 4 1 2 3 2 1 8 0 0 0 0 8 0 2 2
2 3 0 1 2 4 4 1 2 3 0 4 2 3 4 1 2 3 0 2 2 8 8 8 8 8 8 1 2 3
3 0 1 2 3 4 4 2 3 4 1 2 3 0 4 2 3 0 4 2 3 0 1 2 3 0 1 2 2 0
0 4 2 3 0 4 2 3 0 1 2 3 0 1 4 3 0 1 2 2 0 1 2 3 0 1 2 3 2 1
1 2 3 0 1 4 3 4 1 2 3 0 1 2 4 0 1 2 3 2 4 2 3 0 1 2 3 0 2 2
2 3 0 1 2 4 0 1 2 3 0 1 2 3 4 1 4 3 4 2 2 4 0 1 2 3 0 1 2 3
3 0 1 2 3 4 1 2 3 0 4 2 3 0 4 4 3 0 1 2 3 0 1 2 3 0 4 2 2 0
0 1 2 3 0 4 2 3 0 1 2 3 0 1 4 3 0 1 2 2 0 1 2 3 0 1 2 3 2 1
1 2 3 0 4 4 4 0 1 2 3 0 1 2 4 0 1 2 3 2 1 8 8 8 8 8 8 0 2 2
2 3 0 1 2 4 0 8 8 8 8 8 8 3 4 1 2 3 0 2 2 8 0 0 2 0 8 1 2 3
3 0 1 2 4 4 1 8 4 0 4 4 8 0 4 4 3 0 1 2 3 8 2 2 2 0 8 2 2 0
0 1 2 3 0 4 4 8 0 0 4 4 8 1 4 3 0 1 2 2 0 8 0 0 0 0 8 3 2 1
1 2 3 0 1 4 4 8 4 0 0 0 8 2 4 0 1 2 3 2 1 8 0 2 2 0 8 0 2 2
2 3 0 1 4 4 0 8 4 0 4 4 8 4 4 1 2 3 4 2 2 8 8 8 8 8 8 1 2 3
3 0 1 2 3 4 1 8 8 8 8 8 8 0 4 2 3 0 1 2 3 0 0 0 0 0 0 4 2 0
0 1 2 3 0 4 2 3 0 1 2 3 0 1 4 3 0 1 2 2 2 2 2 2 2 2 2 2 2 1
1 2 3 0 1 4 4 4 4 4 4 4 4 4 4 0 1 2 3 0 4 2 3 0 4 2 3 0 1 2
```


**output:**
```
2 2 0 2
0 0 0 2
2 2 2 2
2 0 0 2
```

Okay, let's break down the transformation logic for this task.

**Perception**

1.  **Input Structure:** The input grids are large (30x30) and contain a mix of background noise (often repeating sequences like 1,2,3,4) and distinct geometric objects.
2.  **Key Objects:** The relevant objects appear to be:
    *   **Solid Blocks:** Large, contiguous rectangular areas of a single color (like the red block in `train_1`). White (0) and Gray (5) likely don't count as primary block colors.
    *   **Framed Objects:** Objects consisting of a colored border (e.g., yellow=4 or azure=8), a white (0) interior, and sometimes a smaller, single-colored shape entirely within that white interior (e.g., magenta=6, yellow=4, red=2).
3.  **Relationships:** The crucial relationship seems to be containment – whether a "Framed Object" is located entirely inside a "Solid Block".
4.  **Output Structure:** The output grids are small (5x5 or 4x4) and seem to be constructed based on colors derived from a selected "Framed Object" and its potential container "Solid Block". The pattern of the output grid depends on whether the selected Framed Object was contained within a Solid Block.

**Facts**


```yaml
elements:
  - type: grid
    role: input
    properties:
      size: large (e.g., 30x30)
      content: contains background noise and distinct objects
  - type: grid
    role: output
    properties:
      size: small (e.g., 5x5 or 4x4)
      content: abstract representation based on input objects/colors
  - type: object
    name: solid_block
    properties:
      definition: largest contiguous rectangle of a single color (excluding white/gray)
      attributes:
        - color (container_color)
        - location
        - size
  - type: object
    name: framed_object
    properties:
      definition: object with a colored border, white interior, and a single inner shape of a third color
      attributes:
        - border_color
        - interior_color (always white=0)
        - inner_color
        - inner_shape_pattern (e.g., cross, H, L)
        - location
        - contained_within_solid_block (boolean)

relationships:
  - type: spatial
    description: A framed_object can be located entirely inside a solid_block.

actions:
  - name: identify_candidates
    input: input_grid
    output: list of framed_objects matching the definition
  - name: identify_container
    input: input_grid
    output: the single largest solid_block (if one exists)
  - name: select_target_object
    input: list of candidate framed_objects, container_object (or null)
    output: the single framed_object relevant for output generation
    logic: |
      1. Prioritize candidates contained within the container_object.
      2. If containment exists, select the top-leftmost contained candidate.
      3. If no containment exists, select the candidate with the lowest inner_color value (breaking ties with top-leftmost position).
  - name: extract_colors
    input: target_object, container_object (or null)
    output: inner_color, interior_color (0), primary_color
    logic: |
      inner_color = target_object.inner_color
      interior_color = 0
      primary_color = container_object.color if target_object is contained, else target_object.inner_color
  - name: generate_output_grid
    input: inner_color, interior_color, primary_color, is_contained
    output: output_grid
    logic: |
      If is_contained:
        Construct a 5x5 grid using a fixed pattern with inner_color, primary_color, and interior_color.
      Else:
        Construct a 4x4 grid using a fixed pattern with primary_color (which equals inner_color) and interior_color.
```


**Natural Language Program**

1.  **Identify Candidate Framed Objects:** Find all objects within the input grid that consist of a border of a single color, surrounding an area filled entirely with white (0), which in turn contains a single, contiguous shape of a third distinct color. Record the `inner_color` for each candidate.
2.  **Identify Largest Solid Container:** Find the largest solid rectangular block of a single color (excluding white=0 and gray=5) in the input grid. Note its color (`container_color`) and boundaries. If no such block exists or is unambiguous, consider the container as absent.
3.  **Select the Target Framed Object:**
    *   Check if any identified candidate framed objects lie completely within the boundaries of the largest solid container.
    *   If one or more candidates are contained, select the top-leftmost one as the "target object". Mark this case as `contained`.
    *   If *no* candidates are contained within the largest solid block, select the candidate object that has the numerically smallest `inner_color`. If there's a tie in `inner_color`, choose the top-leftmost one among them. Mark this case as `not_contained`.
4.  **Determine Output Colors:**
    *   Get the `inner_color` from the target object.
    *   The `interior_color` is always white (0).
    *   If the case is `contained`, the `primary_color` is the `container_color` identified in step 2.
    *   If the case is `not_contained`, the `primary_color` is the same as the `inner_color` of the target object.
5.  **Construct Output Grid:**
    *   If the case is `contained`: Create a 5x5 grid following this pattern:
        
```
        Row 1: interior, interior, interior, interior, interior
        Row 2: inner,    primary,  primary,  primary,  primary
        Row 3: primary,  interior, interior, interior, interior
        Row 4: primary,  interior, interior, interior, interior
        Row 5: primary,  interior, interior, interior, interior
        ```

        (Using the colors determined in step 4).
    *   If the case is `not_contained`: Create a 4x4 grid following this pattern:
        
```
        Row 1: primary,  primary,  interior, primary
        Row 2: interior, interior, interior, primary
        Row 3: primary,  primary,  primary,  primary
        Row 4: primary,  interior, interior, primary
        ```

        (Using the colors determined in step 4, where `primary_color == inner_color`).
```python
import numpy as np
from collections import deque

"""
Identify candidate 'framed objects' in the input grid. A framed object has a border of one color, an interior of white (0), and a single contiguous inner shape of a third color.
Identify the largest solid rectangular block of a single color (excluding white=0 and gray=5), which acts as a potential container.
Select the target framed object:
  - If any framed objects are fully contained within the largest solid block, choose the top-leftmost one. Mark this as 'contained'.
  - Otherwise, choose the framed object with the numerically smallest inner color. Break ties using the top-leftmost position. Mark this as 'not_contained'.
Determine output colors:
  - inner_color: The color of the inner shape of the target framed object.
  - interior_color: Always white (0).
  - primary_color: If 'contained', it's the color of the container block. If 'not_contained', it's the inner_color.
Construct the output grid:
  - If 'contained', create a 5x5 grid using a specific pattern with inner_color, primary_color, and interior_color.
  - If 'not_contained', create a 4x4 grid using a specific pattern with primary_color (which equals inner_color) and interior_color.
"""

def find_objects(grid, colors_to_find=None, colors_to_ignore=None):
    """
    Finds all contiguous objects of specified colors in the grid.

    Args:
        grid (np.array): The input grid.
        colors_to_find (set): Set of colors to look for. If None, find all colors not ignored.
        colors_to_ignore (set): Set of colors to ignore.

    Returns:
        list: A list of objects. Each object is a dictionary containing:
              'color': The color of the object.
              'pixels': A set of (row, col) tuples for the object's pixels.
              'bbox': A tuple (min_row, min_col, max_row, max_col) representing the bounding box.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    if colors_to_ignore is None:
        colors_to_ignore = set()

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if not visited[r, c] and color not in colors_to_ignore and \
               (colors_to_find is None or color in colors_to_find):
                
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def is_framed_object(grid, obj_pixels, obj_color, bbox):
    """
    Checks if a set of pixels represents a framed object.
    This is a simplified check focusing on the presence of an inner white area
    and a single non-white, non-border color shape within it.

    Args:
        grid (np.array): The input grid.
        obj_pixels (set): The pixels belonging to the potential frame.
        obj_color (int): The color of the potential frame.
        bbox (tuple): The bounding box of the potential frame.

    Returns:
        tuple: (bool, int or None) - (True if it's a framed object, inner_color)
               or (False, None)
    """
    min_r, min_c, max_r, max_c = bbox
    
    # Check if the bounding box area inside the frame contains white (0)
    has_white_inside = False
    inner_pixels = []
    for r in range(min_r + 1, max_r):
        for c in range(min_c + 1, max_c):
            if (r,c) not in obj_pixels:
                 inner_pixels.append((r,c))
                 if grid[r,c] == 0:
                     has_white_inside = True

    if not has_white_inside or not inner_pixels:
        return False, None

    # Find connected components within the bounding box, *excluding* the frame pixels
    inner_objects = []
    visited_inner = set(obj_pixels) # Don't search starting from the frame

    for r_inner, c_inner in inner_pixels:
         if (r_inner, c_inner) not in visited_inner:
            color = grid[r_inner, c_inner]
            component_pixels = set()
            q = deque([(r_inner, c_inner)])
            visited_inner.add((r_inner, c_inner))
            is_valid_component = True

            while q:
                row, col = q.popleft()
                # Ensure component stays within the bounding box defined by frame
                if not (min_r < row < max_r and min_c < col < max_c):
                    # This component touches/crosses the frame boundary - invalid inner shape definition
                    # This check might be too strict depending on how frame is defined.
                    # Let's allow touching the inner boundary for now. Revisit if needed.
                    pass

                component_pixels.add((row, col))

                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc
                    # Check neighbor is within bounds, not part of the frame, not visited, and same color
                    if min_r <= nr <= max_r and min_c <= nc <= max_c and \
                       (nr, nc) not in obj_pixels and \
                       (nr, nc) not in visited_inner and \
                       grid[nr, nc] == color:
                        visited_inner.add((nr, nc))
                        q.append((nr, nc))

            if is_valid_component and color != 0: # Add only non-white components
                 inner_objects.append({'color': color, 'pixels': component_pixels})
            # We might also want to collect the white component to ensure it's contiguous,
            # but let's keep it simpler first.


    # A valid framed object should have exactly one non-white inner object,
    # and its color should be different from the frame color.
    if len(inner_objects) == 1 and inner_objects[0]['color'] != obj_color:
        return True, inner_objects[0]['color']
    
    return False, None


def find_largest_solid_block(grid, colors_to_ignore):
    """Finds the largest solid rectangular block of a single color, ignoring specified colors."""
    rows, cols = grid.shape
    max_area = -1
    largest_block = None # Store {'color': c, 'bbox': (r, c, r+h-1, c+w-1)}

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color in colors_to_ignore:
                continue

            # Check max possible width from this point
            max_w = 0
            for w in range(1, cols - c + 1):
                if grid[r, c + w - 1] == color:
                    max_w = w
                else:
                    break
            
            # Check height for each potential width
            for w in range(1, max_w + 1):
                h = 0
                for current_h in range(1, rows - r + 1):
                    is_solid = True
                    # Check if the entire row segment matches the color
                    for k in range(w):
                        if grid[r + current_h - 1, c + k] != color:
                            is_solid = False
                            break
                    if is_solid:
                        h = current_h
                    else:
                        break # Height expansion stops here for width w
                
                # Update largest block if current one is bigger
                area = w * h
                if area > max_area:
                    max_area = area
                    largest_block = {'color': color, 'bbox': (r, c, r + h - 1, c + w - 1)}
                elif area == max_area and largest_block is not None:
                     # Tie-breaking: top-leftmost
                     current_bbox = (r, c, r + h - 1, c + w - 1)
                     if current_bbox[0] < largest_block['bbox'][0] or \
                        (current_bbox[0] == largest_block['bbox'][0] and current_bbox[1] < largest_block['bbox'][1]):
                         largest_block = {'color': color, 'bbox': current_bbox}


    return largest_block

def is_contained(inner_bbox, outer_bbox):
    """Checks if inner_bbox is strictly inside outer_bbox."""
    if outer_bbox is None:
        return False
    min_r_in, min_c_in, max_r_in, max_c_in = inner_bbox
    min_r_out, min_c_out, max_r_out, max_c_out = outer_bbox
    return min_r_out <= min_r_in and min_c_out <= min_c_in and \
           max_r_in <= max_r_out and max_c_in <= max_c_out

def transform(input_grid):
    """
    Transforms the input grid based on finding framed objects and a container block.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape

    # 1. Identify Candidate Framed Objects
    candidate_objects = []
    # Find all objects first, excluding only white=0 initially might be better
    # Then filter them based on frame structure
    all_objects = find_objects(grid, colors_to_ignore={0}) # Find non-white objects

    for obj in all_objects:
        is_framed, inner_color = is_framed_object(grid, obj['pixels'], obj['color'], obj['bbox'])
        if is_framed:
            candidate_objects.append({
                'inner_color': inner_color,
                'bbox': obj['bbox'],
                'frame_color': obj['color'] # Keep frame color for potential later use
            })

    if not candidate_objects:
        # Handle cases where no framed objects are found (return empty or default?)
        # Based on examples, this shouldn't happen, but good practice.
        # Let's assume one will always be found according to the task logic.
        # If not, maybe return a small grid of 0s?
         return [[0]] * 3 # Placeholder for error/no object

    # 2. Identify Largest Solid Container
    container_block = find_largest_solid_block(grid, colors_to_ignore={0, 5}) # Ignore white and gray

    # 3. Select the Target Framed Object
    contained_candidates = []
    if container_block:
        container_bbox = container_block['bbox']
        for cand in candidate_objects:
            if is_contained(cand['bbox'], container_bbox):
                contained_candidates.append(cand)

    target_object = None
    is_contained_flag = False

    if contained_candidates:
        # Sort by top-left position (row first, then column)
        contained_candidates.sort(key=lambda x: (x['bbox'][0], x['bbox'][1]))
        target_object = contained_candidates[0]
        is_contained_flag = True
    else:
        # No contained candidates, sort by inner_color, then top-left position
        candidate_objects.sort(key=lambda x: (x['inner_color'], x['bbox'][0], x['bbox'][1]))
        target_object = candidate_objects[0]
        is_contained_flag = False

    # 4. Determine Output Colors
    inner_color = target_object['inner_color']
    interior_color = 0 # Always white

    if is_contained_flag:
        primary_color = container_block['color']
    else:
        primary_color = inner_color # Use inner color as primary if not contained

    # 5. Construct Output Grid
    if is_contained_flag:
        # 5x5 pattern
        output_grid = np.full((5, 5), interior_color, dtype=int)
        # Row 1 is already interior_color
        output_grid[1, 0] = inner_color
        output_grid[1, 1:] = primary_color
        output_grid[2:, 0] = primary_color
        # Rows 3, 4, 5 columns 1-4 are already interior_color
    else:
        # 4x4 pattern
        output_grid = np.full((4, 4), primary_color, dtype=int) # Start filled with primary
        output_grid[0, 2] = interior_color
        output_grid[1, 0:3] = interior_color
        # Row 2 is already primary_color
        output_grid[3, 1:3] = interior_color

    return output_grid.tolist()
```
```python
import numpy as np
from collections import deque

"""
Transformation Rule:

1.  **Identify Candidate Framed Objects:** Find all objects in the input grid that consist of a contiguous border of a single color (frame_color), surrounding an area filled entirely with white (0), which in turn contains a single, contiguous shape of a third distinct color (inner_color, different from frame_color). Record the `inner_color`, `frame_color`, and bounding box (`bbox`) for each candidate.
2.  **Identify Largest Object (Potential Container):** Find the object with the largest number of pixels, excluding white (0) and gray (5). If multiple objects have the same largest pixel count, choose the one whose bounding box is top-leftmost. Note its color (`container_color`) and bounding box (`container_bbox`). If no such object exists, consider the container absent.
3.  **Select the Target Framed Object:**
    *   Identify candidates whose bounding box (`bbox`) is entirely within the `container_bbox`.
    *   From these potentially contained candidates, filter further: only keep those where the `frame_color` is *different* from the `container_color`.
    *   If one or more candidates remain after this filtering (i.e., are geometrically contained *and* have a different frame color than the container), select the top-leftmost one among them as the "target object". Mark this case as `contained`.
    *   If *no* candidates meet both containment criteria, select the candidate object (from the *original* list of all framed objects found in step 1) that has the numerically smallest `inner_color`. If there's a tie in `inner_color`, choose the top-leftmost one among them. Mark this case as `not_contained`.
4.  **Determine Output Colors:**
    *   Get the `inner_color` from the target object.
    *   The `interior_color` is always white (0).
    *   If the case is `contained`, the `primary_color` is the `container_color` identified in step 2.
    *   If the case is `not_contained`, the `primary_color` is the same as the `inner_color` of the target object.
5.  **Construct Output Grid:**
    *   If the case is `contained`: Create a 5x5 grid following the specific pattern:
        Row 1: [0, 0, 0, 0, 0]
        Row 2: [inner, primary, primary, primary, primary]
        Row 3: [primary, 0, 0, 0, 0]
        Row 4: [primary, 0, 0, 0, 0]
        Row 5: [primary, 0, 0, 0, 0]
    *   If the case is `not_contained`: Create a 4x4 grid following the specific pattern:
        Row 1: [primary, primary, 0, primary]
        Row 2: [0, 0, 0, primary]
        Row 3: [primary, primary, primary, primary]
        Row 4: [primary, 0, 0, primary]
"""

def find_objects(grid, colors_to_find=None, colors_to_ignore=None):
    """
    Finds all contiguous objects of specified colors in the grid using 4-connectivity.

    Args:
        grid (np.array): The input grid.
        colors_to_find (set): Set of colors to look for. If None, find all colors not ignored.
        colors_to_ignore (set): Set of colors to ignore.

    Returns:
        list: A list of objects. Each object is a dictionary containing:
              'color': The color of the object.
              'pixels': A set of (row, col) tuples for the object's pixels.
              'bbox': A tuple (min_row, min_col, max_row, max_col) representing the bounding box.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    if colors_to_ignore is None:
        colors_to_ignore = set()

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if not visited[r, c] and color not in colors_to_ignore and \
               (colors_to_find is None or color in colors_to_find):
                
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def is_framed_object_strict(grid, frame_obj):
    """
    Checks if a given object (frame_obj) acts as a frame for an inner object.
    Checks:
    1. Interior region exists within the frame's bounding box.
    2. Interior region (excluding frame pixels) contains only white (0) and exactly one other contiguous non-white object (inner_obj).
    3. The inner_obj's color is different from the frame_obj's color.
    4. The inner_obj does not touch the bounding box edges (it's fully contained within frame space).

    Args:
        grid (np.array): The input grid.
        frame_obj (dict): A potential frame object from find_objects.

    Returns:
        tuple: (bool, int or None) - (True if valid framed object, inner_color)
               or (False, None)
    """
    frame_pixels = frame_obj['pixels']
    frame_color = frame_obj['color']
    min_r, min_c, max_r, max_c = frame_obj['bbox']
    rows, cols = grid.shape

    # Bounding box must allow for an interior
    if max_r - min_r < 2 or max_c - min_c < 2:
        return False, None

    inner_components = []
    visited_inner = set(frame_pixels) # Start by marking frame as visited
    has_white_inside = False

    # Iterate through the potential interior area defined by the bounding box
    for r in range(min_r + 1, max_r):
        for c in range(min_c + 1, max_c):
            if (r, c) not in visited_inner:
                color = grid[r, c]
                
                # Start BFS for this component
                component_pixels = set()
                q = deque([(r, c)])
                visited_inner.add((r, c))
                component_min_r, component_min_c = r, c
                component_max_r, component_max_c = r, c
                
                is_valid_component_boundary = True

                while q:
                    row, col = q.popleft()

                    # Check if component touches the bounding box boundary - disqualifies inner objects
                    # This ensures the inner shape is truly 'inside'
                    if row <= min_r or row >= max_r or col <= min_c or col >= max_c:
                       # This can happen if the frame is not fully enclosing
                       # Let's just skip adding this component if it touches bbox boundary
                       is_valid_component_boundary = False
                       # No need to break, just mark and continue BFS to mark all visited
                       
                    component_pixels.add((row, col))
                    component_min_r = min(component_min_r, row)
                    component_min_c = min(component_min_c, col)
                    component_max_r = max(component_max_r, row)
                    component_max_c = max(component_max_c, col)

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check neighbor is within grid, not visited, and not part of the frame
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited_inner and \
                           (nr, nc) not in frame_pixels and \
                           grid[nr, nc] == color:
                             
                            visited_inner.add((nr, nc))
                            q.append((nr, nc))
                
                # Store the component if it's non-white and didn't touch bbox boundary
                if color == 0:
                    has_white_inside = True
                elif is_valid_component_boundary: # Only consider non-white, non-boundary touching shapes
                     inner_components.append({
                         'color': color, 
                         'pixels': component_pixels,
                         'bbox': (component_min_r, component_min_c, component_max_r, component_max_c)
                     })

    # Check final conditions:
    # 1. Must have found white pixels inside.
    # 2. Must have found exactly one non-white inner component.
    # 3. The inner component's color must differ from the frame color.
    if has_white_inside and len(inner_components) == 1 and inner_components[0]['color'] != frame_color:
        # Optional check: Ensure all pixels inside bbox are either frame, white or inner obj
        # This guards against stray pixels.
        all_interior_pixels = set((r, c) for r in range(min_r + 1, max_r) for c in range(min_c + 1, max_c))
        covered_pixels = frame_pixels.union(inner_components[0]['pixels'])
        
        is_fully_explained = True
        for r_int, c_int in all_interior_pixels:
             if (r_int, c_int) not in covered_pixels and grid[r_int, c_int] != 0 :
                  is_fully_explained = False
                  break
        
        if is_fully_explained:
            return True, inner_components[0]['color']

    return False, None


def find_largest_object_by_pixels(grid, colors_to_ignore):
    """Finds the object with the most pixels, ignoring specified colors."""
    all_objs = find_objects(grid, colors_to_ignore=colors_to_ignore)
    
    if not all_objs:
        return None

    largest_obj = None
    max_pixels = -1

    for obj in all_objs:
        num_pixels = len(obj['pixels'])
        if num_pixels > max_pixels:
            max_pixels = num_pixels
            largest_obj = obj
        elif num_pixels == max_pixels:
            # Tie-breaking: top-leftmost bounding box
            current_bbox = obj['bbox']
            if current_bbox[0] < largest_obj['bbox'][0] or \
               (current_bbox[0] == largest_obj['bbox'][0] and current_bbox[1] < largest_obj['bbox'][1]):
                largest_obj = obj
                
    return largest_obj

def is_contained(inner_bbox, outer_bbox):
    """Checks if inner_bbox is strictly inside or touching the boundaries of outer_bbox."""
    if outer_bbox is None or inner_bbox is None:
        return False
    min_r_in, min_c_in, max_r_in, max_c_in = inner_bbox
    min_r_out, min_c_out, max_r_out, max_c_out = outer_bbox
    return min_r_out <= min_r_in and min_c_out <= min_c_in and \
           max_r_in <= max_r_out and max_c_in <= max_c_out


def transform(input_grid):
    grid = np.array(input_grid, dtype=int)

    # 1. Identify Candidate Framed Objects
    candidate_objects = []
    # Find all non-white, non-gray potential frames first
    potential_frames = find_objects(grid, colors_to_ignore={0, 5}) 

    for p_frame in potential_frames:
        is_framed, inner_color = is_framed_object_strict(grid, p_frame)
        if is_framed:
            candidate_objects.append({
                'inner_color': inner_color,
                'bbox': p_frame['bbox'],
                'frame_color': p_frame['color'] 
            })

    if not candidate_objects:
         # Fallback if no valid framed objects found
         # This case wasn't explicitly defined by examples, return small default
         return [[0]] 

    # 2. Identify Largest Object (Potential Container)
    container_object = find_largest_object_by_pixels(grid, colors_to_ignore={0, 5}) # Ignore white and gray

    # 3. Select the Target Framed Object
    valid_contained_candidates = []
    if container_object:
        container_bbox = container_object['bbox']
        container_color = container_object['color']
        for cand in candidate_objects:
            # Check geometric containment AND different frame/container color
            if is_contained(cand['bbox'], container_bbox) and cand['frame_color'] != container_color:
                valid_contained_candidates.append(cand)

    target_object = None
    is_contained_flag = False

    if valid_contained_candidates:
        # Sort by top-left position (row first, then column)
        valid_contained_candidates.sort(key=lambda x: (x['bbox'][0], x['bbox'][1]))
        target_object = valid_contained_candidates[0]
        is_contained_flag = True
    else:
        # No valid contained candidates, sort ALL candidates by inner_color, then top-left
        candidate_objects.sort(key=lambda x: (x['inner_color'], x['bbox'][0], x['bbox'][1]))
        target_object = candidate_objects[0]
        is_contained_flag = False

    # 4. Determine Output Colors
    inner_color = target_object['inner_color']
    interior_color = 0 # Always white

    if is_contained_flag:
        # Container must exist if is_contained_flag is True
        primary_color = container_object['color']
    else:
        primary_color = inner_color # Use inner color as primary if not contained

    # 5. Construct Output Grid
    if is_contained_flag:
        # 5x5 pattern
        output_grid = np.full((5, 5), interior_color, dtype=int)
        output_grid[1, 0] = inner_color
        output_grid[1, 1:] = primary_color
        output_grid[2:, 0] = primary_color
    else:
        # 4x4 pattern
        output_grid = np.full((4, 4), primary_color, dtype=int) # Start filled with primary
        output_grid[0, 2] = interior_color
        output_grid[1, 0:3] = interior_color
        # Row 2 is filled with primary
        output_grid[3, 1:3] = interior_color

    return output_grid.tolist()
```
```python
import numpy as np
from collections import deque

"""
Transformation Rule:

1.  **Identify Candidate Framed Objects:** Find all objects in the input grid that consist of a contiguous border of a single color (frame_color), surrounding an area filled entirely with white (0), which in turn contains a single, contiguous shape of a third distinct color (inner_color, different from frame_color). Record the `inner_color`, `frame_color`, and bounding box (`bbox`) for each candidate.
2.  **Identify Largest Solid Rectangular Block (Potential Container):** Find the solid rectangular block with the largest area, consisting of a single color excluding white (0) and gray (5). If multiple blocks share the maximum area, choose the one whose top-left corner is highest, breaking further ties by choosing the leftmost one. Note its color (`container_color`) and bounding box (`container_bbox`). If no such block exists, consider the container absent.
3.  **Select the Target Framed Object:**
    *   Identify candidate framed objects whose bounding box (`bbox`) is entirely within the `container_bbox`.
    *   If one or more candidates are contained within the container block's bounding box, select the one whose top-left corner is highest, breaking further ties by choosing the leftmost one. This is the "target object". Mark this case as `contained`.
    *   If *no* candidates are contained within the container block's bounding box, select the candidate object (from the *original* list of all framed objects found in step 1) that has the numerically smallest `inner_color`. If there's a tie in `inner_color`, choose the one whose top-left corner is highest, breaking further ties by choosing the leftmost one. This is the "target object". Mark this case as `not_contained`.
4.  **Determine Output Colors:**
    *   Get the `inner_color` from the target object.
    *   The `interior_color` is always white (0).
    *   If the case is `contained`, the `primary_color` is the `container_color` identified in step 2.
    *   If the case is `not_contained`, the `primary_color` is the same as the `inner_color` of the target object.
5.  **Construct Output Grid:**
    *   If the case is `contained`: Create a 5x5 grid following the specific pattern:
        Row 1: [0, 0, 0, 0, 0]
        Row 2: [inner, primary, primary, primary, primary]
        Row 3: [primary, 0, 0, 0, 0]
        Row 4: [primary, 0, 0, 0, 0]
        Row 5: [primary, 0, 0, 0, 0]
    *   If the case is `not_contained`: Create a 4x4 grid following the specific pattern:
        Row 1: [primary, primary, 0, primary]
        Row 2: [0, 0, 0, primary]
        Row 3: [primary, primary, primary, primary]
        Row 4: [primary, 0, 0, primary]
"""

def find_objects(grid, colors_to_find=None, colors_to_ignore=None):
    """
    Finds all contiguous objects of specified colors in the grid using 4-connectivity.

    Args:
        grid (np.array): The input grid.
        colors_to_find (set): Set of colors to look for. If None, find all colors not ignored.
        colors_to_ignore (set): Set of colors to ignore.

    Returns:
        list: A list of objects. Each object is a dictionary containing:
              'color': The color of the object.
              'pixels': A set of (row, col) tuples for the object's pixels.
              'bbox': A tuple (min_row, min_col, max_row, max_col) representing the bounding box.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    if colors_to_ignore is None:
        colors_to_ignore = set()

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Process pixel if not visited, not ignored, and either find all or in specific set
            if not visited[r, c] and color not in colors_to_ignore and \
               (colors_to_find is None or color in colors_to_find):
                
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                # Breadth-First Search (BFS) to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    # Update bounding box
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor is same color and not visited
                            if not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                # Store the found object
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def is_framed_object_strict(grid, frame_obj):
    """
    Checks if a given object (frame_obj) acts as a valid frame for an inner object.
    Checks:
    1. A potential interior region exists within the frame's bounding box.
    2. The region inside the bounding box but excluding frame pixels contains white (0).
    3. This interior region contains exactly one contiguous non-white object (inner_obj).
    4. The inner_obj's color is different from the frame_obj's color.
    5. The inner_obj does not touch the outer edges of the frame's bounding box.
    6. All non-frame pixels within the bounding box are either white or part of the single inner object.

    Args:
        grid (np.array): The input grid.
        frame_obj (dict): A potential frame object from find_objects.

    Returns:
        tuple: (bool, int or None) - (True if valid framed object, inner_color)
               or (False, None)
    """
    frame_pixels = frame_obj['pixels']
    frame_color = frame_obj['color']
    min_r, min_c, max_r, max_c = frame_obj['bbox']
    rows, cols = grid.shape

    # Frame bounding box must be large enough to potentially contain something
    if max_r - min_r < 2 or max_c - min_c < 2:
        return False, None

    inner_components = [] # Stores non-white components found inside
    visited_inner = set(frame_pixels) # Mark frame pixels as visited for the inner search
    has_white_inside = False
    all_interior_pixels = set() # Track all pixels scanned inside the bbox (excluding frame)

    # Iterate through the potential interior area (inside the bounding box)
    for r in range(min_r + 1, max_r):
        for c in range(min_c + 1, max_c):
            # Skip if this pixel is part of the frame or already visited
            if (r, c) not in visited_inner:
                all_interior_pixels.add((r,c)) # Mark this as an interior pixel
                color = grid[r, c]
                
                # Start BFS for this component within the interior
                component_pixels = set()
                q = deque([(r, c)])
                visited_inner.add((r, c))
                is_valid_inner_component = True # Assume valid until it touches bbox boundary

                while q:
                    row, col = q.popleft()
                    component_pixels.add((row, col))

                    # Check if component touches the bounding box boundary - disqualifies non-white inner objects
                    if row <= min_r or row >= max_r or col <= min_c or col >= max_c:
                       is_valid_inner_component = False # Mark as invalid if touching bbox edge
                       # Continue BFS to mark all pixels of this invalid component as visited

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check neighbor is within grid, not visited, not frame, and same color
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited_inner and \
                           (nr, nc) not in frame_pixels and \
                           grid[nr, nc] == color:
                            
                            visited_inner.add((nr, nc))
                            q.append((nr, nc))
                
                # After BFS for the component, decide what it was
                if color == 0:
                    has_white_inside = True
                    # We don't store the white component explicitly, just note its presence
                elif is_valid_inner_component: # Only store non-white components fully inside
                     inner_components.append({
                         'color': color, 
                         'pixels': component_pixels,
                     })

    # Check final conditions for a valid framed object:
    # 1. Must have found white pixels inside the frame's bbox.
    # 2. Must have found exactly one valid (non-boundary touching) non-white inner component.
    # 3. The inner component's color must differ from the frame color.
    # 4. Check if all interior pixels are accounted for (frame, white, or the single inner object)
    if has_white_inside and len(inner_components) == 1 and inner_components[0]['color'] != frame_color:
        # Check if all visited inner pixels belong to the found inner component or were white
        inner_pixels_found = inner_components[0]['pixels']
        is_fully_explained = True
        for p in all_interior_pixels:
            if p not in inner_pixels_found and grid[p] != 0:
                 is_fully_explained = False
                 break 
        
        if is_fully_explained:
            return True, inner_components[0]['color']

    return False, None

def find_largest_solid_block(grid, colors_to_ignore):
    """Finds the largest solid rectangular block of a single color, ignoring specified colors."""
    rows, cols = grid.shape
    max_area = -1
    largest_block = None # Store {'color': c, 'bbox': (min_r, min_c, max_r, max_c)}

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Skip ignored colors
            if color in colors_to_ignore:
                continue

            # Determine the maximum possible width starting at (r, c) for this color
            max_w = 0
            for w in range(1, cols - c + 1):
                if grid[r, c + w - 1] == color:
                    max_w = w
                else:
                    break # Width extension stops
            
            # For each possible width, find the maximum height
            for w in range(1, max_w + 1):
                h = 0
                # Check rows downwards
                for current_h in range(1, rows - r + 1):
                    is_solid_row_segment = True
                    # Check if the entire row segment matches the color
                    for k in range(w):
                        if grid[r + current_h - 1, c + k] != color:
                            is_solid_row_segment = False
                            break
                    
                    if is_solid_row_segment:
                        h = current_h # Extend height
                    else:
                        break # Height expansion stops here for width w
                
                # Calculate area and update largest block if needed
                area = w * h
                if area > max_area:
                    max_area = area
                    largest_block = {'color': color, 'bbox': (r, c, r + h - 1, c + w - 1)}
                elif area == max_area and largest_block is not None:
                     # Tie-breaking: top-leftmost (compare top row, then left column)
                     current_bbox = (r, c, r + h - 1, c + w - 1)
                     if current_bbox[0] < largest_block['bbox'][0] or \
                        (current_bbox[0] == largest_block['bbox'][0] and current_bbox[1] < largest_block['bbox'][1]):
                         largest_block = {'color': color, 'bbox': current_bbox}

    return largest_block

def is_contained(inner_bbox, outer_bbox):
    """Checks if inner_bbox is strictly inside or touching the boundaries of outer_bbox."""
    if outer_bbox is None or inner_bbox is None:
        return False
    min_r_in, min_c_in, max_r_in, max_c_in = inner_bbox
    min_r_out, min_c_out, max_r_out, max_c_out = outer_bbox
    # Check if all corners of inner are within or on the boundary of outer
    return min_r_out <= min_r_in and min_c_out <= min_c_in and \
           max_r_in <= max_r_out and max_c_in <= max_c_out

def transform(input_grid):
    """
    Applies the transformation logic to the input grid.
    """
    grid = np.array(input_grid, dtype=int)

    # 1. Identify Candidate Framed Objects
    candidate_objects = []
    # Find all non-white, non-gray objects as potential frames
    potential_frames = find_objects(grid, colors_to_ignore={0, 5}) 

    # Validate each potential frame
    for p_frame in potential_frames:
        is_framed, inner_color = is_framed_object_strict(grid, p_frame)
        if is_framed:
            candidate_objects.append({
                'inner_color': inner_color,
                'bbox': p_frame['bbox'],
                'frame_color': p_frame['color'] # Store frame color, might be useful
            })

    # Handle case where no valid framed objects are found
    if not candidate_objects:
         # Based on ARC tasks, this is unlikely for valid inputs, but return a minimal grid.
         return [[0]] 

    # 2. Identify Largest Solid Rectangular Block (Potential Container)
    container_block = find_largest_solid_block(grid, colors_to_ignore={0, 5}) # Ignore white and gray

    # 3. Select the Target Framed Object
    contained_candidates = []
    if container_block:
        container_bbox = container_block['bbox']
        # Find candidates fully contained within the container's bounding box
        for cand in candidate_objects:
            if is_contained(cand['bbox'], container_bbox):
                contained_candidates.append(cand)

    target_object = None
    is_contained_flag = False

    if contained_candidates:
        # If candidates are contained, select the top-leftmost one
        # Sort by top row (bbox[0]), then left column (bbox[1])
        contained_candidates.sort(key=lambda x: (x['bbox'][0], x['bbox'][1]))
        target_object = contained_candidates[0]
        is_contained_flag = True
    else:
        # If no candidates are contained, select from ALL candidates
        # Sort by inner_color, then top row, then left column
        candidate_objects.sort(key=lambda x: (x['inner_color'], x['bbox'][0], x['bbox'][1]))
        target_object = candidate_objects[0]
        is_contained_flag = False

    # 4. Determine Output Colors
    inner_color = target_object['inner_color']
    interior_color = 0 # Always white

    if is_contained_flag:
        # If contained, primary color is the container's color
        # Container must exist if is_contained_flag is True
        primary_color = container_block['color']
    else:
        # If not contained, primary color is the inner color of the target
        primary_color = inner_color 

    # 5. Construct Output Grid based on whether the target was contained
    if is_contained_flag:
        # Create the 5x5 pattern for contained objects
        output_grid = np.full((5, 5), interior_color, dtype=int) # Fill with white (0)
        output_grid[1, 0] = inner_color # Top-left of second row
        output_grid[1, 1:] = primary_color # Rest of second row
        output_grid[2:, 0] = primary_color # First column, rows 3-5
    else:
        # Create the 4x4 pattern for non-contained objects
        output_grid = np.full((4, 4), primary_color, dtype=int) # Fill with primary color
        # Set specific pixels to interior color (white 0)
        output_grid[0, 2] = interior_color
        output_grid[1, 0:3] = interior_color
        # Row 3 remains primary color
        output_grid[3, 1:3] = interior_color

    # Return the result as a list of lists
    return output_grid.tolist()
```

Previous Code:
```python
import numpy as np
from collections import deque

"""
Transformation Rule:

1.  **Identify Candidate Framed Objects:** Find all objects in the input grid that consist of a contiguous border of a single color (frame_color), surrounding an area filled entirely with white (0), which in turn contains a single, contiguous shape of a third distinct color (inner_color, different from frame_color). Record the `inner_color`, `frame_color`, and bounding box (`bbox`) for each candidate.
2.  **Identify Largest Solid Rectangular Block (Potential Container):** Find the solid rectangular block with the largest area, consisting of a single color excluding white (0) and gray (5). If multiple blocks share the maximum area, choose the one whose top-left corner is highest, breaking further ties by choosing the leftmost one. Note its color (`container_color`) and bounding box (`container_bbox`). If no such block exists, consider the container absent.
3.  **Select the Target Framed Object:**
    *   Identify candidate framed objects whose bounding box (`bbox`) is entirely within the `container_bbox`.
    *   If one or more candidates are contained within the container block's bounding box, select the one whose top-left corner is highest, breaking further ties by choosing the leftmost one. This is the "target object". Mark this case as `contained`.
    *   If *no* candidates are contained within the container block's bounding box, select the candidate object (from the *original* list of all framed objects found in step 1) that has the numerically smallest `inner_color`. If there's a tie in `inner_color`, choose the one whose top-left corner is highest, breaking further ties by choosing the leftmost one. This is the "target object". Mark this case as `not_contained`.
4.  **Determine Output Colors:**
    *   Get the `inner_color` from the target object.
    *   The `interior_color` is always white (0).
    *   If the case is `contained`, the `primary_color` is the `container_color` identified in step 2.
    *   If the case is `not_contained`, the `primary_color` is the same as the `inner_color` of the target object.
5.  **Construct Output Grid:**
    *   If the case is `contained`: Create a 5x5 grid following the specific pattern:
        Row 1: [0, 0, 0, 0, 0]
        Row 2: [inner, primary, primary, primary, primary]
        Row 3: [primary, 0, 0, 0, 0]
        Row 4: [primary, 0, 0, 0, 0]
        Row 5: [primary, 0, 0, 0, 0]
    *   If the case is `not_contained`: Create a 4x4 grid following the specific pattern:
        Row 1: [primary, primary, 0, primary]
        Row 2: [0, 0, 0, primary]
        Row 3: [primary, primary, primary, primary]
        Row 4: [primary, 0, 0, primary]
"""

def find_objects(grid, colors_to_find=None, colors_to_ignore=None):
    """
    Finds all contiguous objects of specified colors in the grid using 4-connectivity.

    Args:
        grid (np.array): The input grid.
        colors_to_find (set): Set of colors to look for. If None, find all colors not ignored.
        colors_to_ignore (set): Set of colors to ignore.

    Returns:
        list: A list of objects. Each object is a dictionary containing:
              'color': The color of the object.
              'pixels': A set of (row, col) tuples for the object's pixels.
              'bbox': A tuple (min_row, min_col, max_row, max_col) representing the bounding box.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    if colors_to_ignore is None:
        colors_to_ignore = set()

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Process pixel if not visited, not ignored, and either find all or in specific set
            if not visited[r, c] and color not in colors_to_ignore and \
               (colors_to_find is None or color in colors_to_find):
                
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                # Breadth-First Search (BFS) to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    # Update bounding box
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor is same color and not visited
                            if not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                # Store the found object
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def is_framed_object_strict(grid, frame_obj):
    """
    Checks if a given object (frame_obj) acts as a valid frame for an inner object.
    Checks:
    1. A potential interior region exists within the frame's bounding box.
    2. The region inside the bounding box but excluding frame pixels contains white (0).
    3. This interior region contains exactly one contiguous non-white object (inner_obj).
    4. The inner_obj's color is different from the frame_obj's color.
    5. The inner_obj does not touch the outer edges of the frame's bounding box.
    6. All non-frame pixels within the bounding box are either white or part of the single inner object.

    Args:
        grid (np.array): The input grid.
        frame_obj (dict): A potential frame object from find_objects.

    Returns:
        tuple: (bool, int or None) - (True if valid framed object, inner_color)
               or (False, None)
    """
    frame_pixels = frame_obj['pixels']
    frame_color = frame_obj['color']
    min_r, min_c, max_r, max_c = frame_obj['bbox']
    rows, cols = grid.shape

    # Frame bounding box must be large enough to potentially contain something
    if max_r - min_r < 2 or max_c - min_c < 2:
        return False, None

    inner_components = [] # Stores non-white components found inside
    visited_inner = set(frame_pixels) # Mark frame pixels as visited for the inner search
    has_white_inside = False
    all_interior_pixels = set() # Track all pixels scanned inside the bbox (excluding frame)

    # Iterate through the potential interior area (inside the bounding box)
    for r in range(min_r + 1, max_r):
        for c in range(min_c + 1, max_c):
            # Skip if this pixel is part of the frame or already visited
            if (r, c) not in visited_inner:
                all_interior_pixels.add((r,c)) # Mark this as an interior pixel
                color = grid[r, c]
                
                # Start BFS for this component within the interior
                component_pixels = set()
                q = deque([(r, c)])
                visited_inner.add((r, c))
                is_valid_inner_component = True # Assume valid until it touches bbox boundary

                while q:
                    row, col = q.popleft()
                    component_pixels.add((row, col))

                    # Check if component touches the bounding box boundary - disqualifies non-white inner objects
                    if row <= min_r or row >= max_r or col <= min_c or col >= max_c:
                       is_valid_inner_component = False # Mark as invalid if touching bbox edge
                       # Continue BFS to mark all pixels of this invalid component as visited

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check neighbor is within grid, not visited, not frame, and same color
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited_inner and \
                           (nr, nc) not in frame_pixels and \
                           grid[nr, nc] == color:
                            
                            visited_inner.add((nr, nc))
                            q.append((nr, nc))
                
                # After BFS for the component, decide what it was
                if color == 0:
                    has_white_inside = True
                    # We don't store the white component explicitly, just note its presence
                elif is_valid_inner_component: # Only store non-white components fully inside
                     inner_components.append({
                         'color': color, 
                         'pixels': component_pixels,
                     })

    # Check final conditions for a valid framed object:
    # 1. Must have found white pixels inside the frame's bbox.
    # 2. Must have found exactly one valid (non-boundary touching) non-white inner component.
    # 3. The inner component's color must differ from the frame color.
    # 4. Check if all interior pixels are accounted for (frame, white, or the single inner object)
    if has_white_inside and len(inner_components) == 1 and inner_components[0]['color'] != frame_color:
        # Check if all visited inner pixels belong to the found inner component or were white
        inner_pixels_found = inner_components[0]['pixels']
        is_fully_explained = True
        for p in all_interior_pixels:
            if p not in inner_pixels_found and grid[p] != 0:
                 is_fully_explained = False
                 break 
        
        if is_fully_explained:
            return True, inner_components[0]['color']

    return False, None

def find_largest_solid_block(grid, colors_to_ignore):
    """Finds the largest solid rectangular block of a single color, ignoring specified colors."""
    rows, cols = grid.shape
    max_area = -1
    largest_block = None # Store {'color': c, 'bbox': (min_r, min_c, max_r, max_c)}

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Skip ignored colors
            if color in colors_to_ignore:
                continue

            # Determine the maximum possible width starting at (r, c) for this color
            max_w = 0
            for w in range(1, cols - c + 1):
                if grid[r, c + w - 1] == color:
                    max_w = w
                else:
                    break # Width extension stops
            
            # For each possible width, find the maximum height
            for w in range(1, max_w + 1):
                h = 0
                # Check rows downwards
                for current_h in range(1, rows - r + 1):
                    is_solid_row_segment = True
                    # Check if the entire row segment matches the color
                    for k in range(w):
                        if grid[r + current_h - 1, c + k] != color:
                            is_solid_row_segment = False
                            break
                    
                    if is_solid_row_segment:
                        h = current_h # Extend height
                    else:
                        break # Height expansion stops here for width w
                
                # Calculate area and update largest block if needed
                area = w * h
                if area > max_area:
                    max_area = area
                    largest_block = {'color': color, 'bbox': (r, c, r + h - 1, c + w - 1)}
                elif area == max_area and largest_block is not None:
                     # Tie-breaking: top-leftmost (compare top row, then left column)
                     current_bbox = (r, c, r + h - 1, c + w - 1)
                     if current_bbox[0] < largest_block['bbox'][0] or \
                        (current_bbox[0] == largest_block['bbox'][0] and current_bbox[1] < largest_block['bbox'][1]):
                         largest_block = {'color': color, 'bbox': current_bbox}

    return largest_block

def is_contained(inner_bbox, outer_bbox):
    """Checks if inner_bbox is strictly inside or touching the boundaries of outer_bbox."""
    if outer_bbox is None or inner_bbox is None:
        return False
    min_r_in, min_c_in, max_r_in, max_c_in = inner_bbox
    min_r_out, min_c_out, max_r_out, max_c_out = outer_bbox
    # Check if all corners of inner are within or on the boundary of outer
    return min_r_out <= min_r_in and min_c_out <= min_c_in and \
           max_r_in <= max_r_out and max_c_in <= max_c_out

def transform(input_grid):
    """
    Applies the transformation logic to the input grid.
    """
    grid = np.array(input_grid, dtype=int)

    # 1. Identify Candidate Framed Objects
    candidate_objects = []
    # Find all non-white, non-gray objects as potential frames
    potential_frames = find_objects(grid, colors_to_ignore={0, 5}) 

    # Validate each potential frame
    for p_frame in potential_frames:
        is_framed, inner_color = is_framed_object_strict(grid, p_frame)
        if is_framed:
            candidate_objects.append({
                'inner_color': inner_color,
                'bbox': p_frame['bbox'],
                'frame_color': p_frame['color'] # Store frame color, might be useful
            })

    # Handle case where no valid framed objects are found
    if not candidate_objects:
         # Based on ARC tasks, this is unlikely for valid inputs, but return a minimal grid.
         return [[0]] 

    # 2. Identify Largest Solid Rectangular Block (Potential Container)
    container_block = find_largest_solid_block(grid, colors_to_ignore={0, 5}) # Ignore white and gray

    # 3. Select the Target Framed Object
    contained_candidates = []
    if container_block:
        container_bbox = container_block['bbox']
        # Find candidates fully contained within the container's bounding box
        for cand in candidate_objects:
            if is_contained(cand['bbox'], container_bbox):
                contained_candidates.append(cand)

    target_object = None
    is_contained_flag = False

    if contained_candidates:
        # If candidates are contained, select the top-leftmost one
        # Sort by top row (bbox[0]), then left column (bbox[1])
        contained_candidates.sort(key=lambda x: (x['bbox'][0], x['bbox'][1]))
        target_object = contained_candidates[0]
        is_contained_flag = True
    else:
        # If no candidates are contained, select from ALL candidates
        # Sort by inner_color, then top row, then left column
        candidate_objects.sort(key=lambda x: (x['inner_color'], x['bbox'][0], x['bbox'][1]))
        target_object = candidate_objects[0]
        is_contained_flag = False

    # 4. Determine Output Colors
    inner_color = target_object['inner_color']
    interior_color = 0 # Always white

    if is_contained_flag:
        # If contained, primary color is the container's color
        # Container must exist if is_contained_flag is True
        primary_color = container_block['color']
    else:
        # If not contained, primary color is the inner color of the target
        primary_color = inner_color 

    # 5. Construct Output Grid based on whether the target was contained
    if is_contained_flag:
        # Create the 5x5 pattern for contained objects
        output_grid = np.full((5, 5), interior_color, dtype=int) # Fill with white (0)
        output_grid[1, 0] = inner_color # Top-left of second row
        output_grid[1, 1:] = primary_color # Rest of second row
        output_grid[2:, 0] = primary_color # First column, rows 3-5
    else:
        # Create the 4x4 pattern for non-contained objects
        output_grid = np.full((4, 4), primary_color, dtype=int) # Fill with primary color
        # Set specific pixels to interior color (white 0)
        output_grid[0, 2] = interior_color
        output_grid[1, 0:3] = interior_color
        # Row 3 remains primary color
        output_grid[3, 1:3] = interior_color

    # Return the result as a list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 2 3 4 1 1 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2
4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1
3 4 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 3 1 4 4 4 4 4 4 4 4 1 2 3 4 1 2 3 4 1 2 3 4 1 1 3 4 1 1 3
1 2 1 4 1 0 0 0 0 4 3 4 1 2 3 4 1 2 3 4 4 4 4 4 4 4 3 4 1 2
4 1 1 4 6 1 1 1 6 4 2 3 4 1 2 3 4 1 2 4 1 0 0 0 0 4 2 3 1 1
3 4 1 4 0 0 0 0 1 4 1 2 3 4 1 2 3 4 1 4 6 0 0 0 6 4 1 2 1 4
1 3 1 4 0 0 0 0 1 4 4 1 2 3 1 1 2 3 1 4 0 0 0 0 0 4 4 1 1 3
1 2 1 4 0 0 0 0 1 4 3 4 1 2 3 4 1 2 3 4 0 0 0 0 0 4 3 4 1 2
4 1 1 4 4 4 4 4 4 4 2 1 4 1 2 3 4 1 2 4 0 0 0 0 1 4 2 3 1 1
3 4 1 2 3 4 1 2 3 4 1 1 3 4 1 2 3 4 1 4 4 4 4 4 4 4 1 2 1 4
1 3 1 1 2 3 4 1 2 3 4 1 1 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 1 3
1 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1
3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 1 4 1 2 3 4 1 1 1 4 1 2 3 4
2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 1 4 1 2 1 4 1 1 3
1 2 3 4 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 2 3 4 1 2
4 1 2 3 4 2 2 3 4 1 2 3 4 1 2 3 4 4 4 4 4 4 4 2 4 1 2 3 4 1
3 4 1 2 3 2 4 4 4 4 4 4 4 4 1 2 4 0 0 0 0 0 4 2 3 4 1 2 3 4
2 3 4 1 2 2 4 0 0 0 0 0 4 3 4 1 4 0 0 0 0 0 4 2 2 1 4 1 2 3
1 2 3 4 1 2 4 6 0 0 0 2 4 2 3 4 4 0 0 0 0 0 4 2 1 2 3 4 1 2
4 1 2 3 4 2 4 0 0 0 0 0 4 1 2 3 4 0 0 0 0 0 4 2 4 1 2 3 4 1
3 4 1 2 3 2 4 0 0 0 0 0 4 1 1 2 4 0 0 0 0 0 4 2 3 4 1 2 3 4
2 3 4 1 2 2 4 2 0 0 0 0 4 3 4 1 4 4 4 4 4 4 4 2 2 3 4 1 2 3
1 2 3 1 1 2 4 4 4 4 4 4 4 2 3 4 1 2 3 4 1 2 3 2 1 2 3 4 1 2
4 1 2 3 4 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 2 3 4 1
3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 1 3 4 1 2 3 4 1 2 3 4 1 2 3 4
2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 1 4 1 2 3 4 1 2 3
1 2 3 4 1 2 3 1 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2
4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1
```
Expected Output:
```
0 0 0 0 0
6 2 2 2 2
2 0 0 0 0
2 0 0 0 0
2 0 0 0 0
```
Transformed Output:
```
0
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None

## Example 2:
Input:
```
4 1 2 3 0 4 4 4 4 4 4 4 4 4 4 3 0 1 2 4 4 1 2 3 4 1 2 4 0 1
1 2 4 0 1 4 3 0 1 2 3 4 1 2 4 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2
2 3 0 1 2 4 0 8 8 8 8 8 8 3 4 1 2 3 0 4 2 3 0 1 4 3 0 1 2 3
3 0 1 2 3 4 1 8 0 4 0 0 8 0 4 2 3 0 1 2 3 0 1 2 3 4 1 2 3 0
0 1 2 3 0 4 2 8 4 4 0 0 8 1 4 3 0 1 2 3 4 4 2 3 0 1 2 3 0 1
1 2 3 0 4 4 4 8 0 4 4 4 8 2 4 0 1 2 3 4 1 2 3 0 1 2 3 0 1 2
2 3 0 1 2 4 0 8 0 4 0 0 8 3 4 1 2 3 4 2 2 2 2 2 2 2 2 2 2 3
3 0 1 2 3 4 1 8 8 8 8 8 8 4 4 2 3 0 1 2 2 2 2 2 2 2 2 2 2 0
0 1 2 3 0 4 2 3 0 1 2 3 0 1 4 3 0 1 2 2 0 1 2 3 0 1 2 3 2 1
1 2 3 0 4 4 4 0 1 2 3 0 1 2 4 0 4 2 3 2 1 8 8 8 8 8 8 0 2 2
2 4 0 1 4 4 0 4 2 3 0 1 2 4 4 1 2 3 0 2 2 8 0 0 0 0 8 1 2 3
3 0 1 2 3 4 1 2 3 0 4 2 3 0 4 4 3 0 1 2 4 8 0 0 0 0 8 2 2 0
4 1 2 3 0 4 2 3 0 1 2 3 4 1 4 4 0 1 2 2 0 8 0 0 0 0 8 3 2 1
1 2 3 0 1 4 3 0 1 2 3 0 1 2 4 4 1 2 3 2 1 8 0 0 0 0 8 0 2 2
2 3 0 1 2 4 4 1 2 3 0 4 2 3 4 1 2 3 0 2 2 8 8 8 8 8 8 1 2 3
3 0 1 2 3 4 4 2 3 4 1 2 3 0 4 2 3 0 4 2 3 0 1 2 3 0 1 2 2 0
0 4 2 3 0 4 2 3 0 1 2 3 0 1 4 3 0 1 2 2 0 1 2 3 0 1 2 3 2 1
1 2 3 0 1 4 3 4 1 2 3 0 1 2 4 0 1 2 3 2 4 2 3 0 1 2 3 0 2 2
2 3 0 1 2 4 0 1 2 3 0 1 2 3 4 1 4 3 4 2 2 4 0 1 2 3 0 1 2 3
3 0 1 2 3 4 1 2 3 0 4 2 3 0 4 4 3 0 1 2 3 0 1 2 3 0 4 2 2 0
0 1 2 3 0 4 2 3 0 1 2 3 0 1 4 3 0 1 2 2 0 1 2 3 0 1 2 3 2 1
1 2 3 0 4 4 4 0 1 2 3 0 1 2 4 0 1 2 3 2 1 8 8 8 8 8 8 0 2 2
2 3 0 1 2 4 0 8 8 8 8 8 8 3 4 1 2 3 0 2 2 8 0 0 2 0 8 1 2 3
3 0 1 2 4 4 1 8 4 0 4 4 8 0 4 4 3 0 1 2 3 8 2 2 2 0 8 2 2 0
0 1 2 3 0 4 4 8 0 0 4 4 8 1 4 3 0 1 2 2 0 8 0 0 0 0 8 3 2 1
1 2 3 0 1 4 4 8 4 0 0 0 8 2 4 0 1 2 3 2 1 8 0 2 2 0 8 0 2 2
2 3 0 1 4 4 0 8 4 0 4 4 8 4 4 1 2 3 4 2 2 8 8 8 8 8 8 1 2 3
3 0 1 2 3 4 1 8 8 8 8 8 8 0 4 2 3 0 1 2 3 0 0 0 0 0 0 4 2 0
0 1 2 3 0 4 2 3 0 1 2 3 0 1 4 3 0 1 2 2 2 2 2 2 2 2 2 2 2 1
1 2 3 0 1 4 4 4 4 4 4 4 4 4 4 0 1 2 3 0 4 2 3 0 4 2 3 0 1 2
```
Expected Output:
```
2 2 0 2
0 0 0 2
2 2 2 2
2 0 0 2
```
Transformed Output:
```
4 4 0 4
0 0 0 4
4 4 4 4
4 0 0 4
```
Match: False
Pixels Off: 10
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 250.0
**General Assessment and Strategy**

The previous code failed on both training examples, indicating fundamental issues in either identifying the correct objects (framed objects, container blocks) or applying the selection logic (containment check, color priority).

*   **Example 1 Failure:** The code returned `[[0]]`, suggesting it failed to identify the necessary components (the framed object or the container block) or incorrectly determined their relationship, leading to an undefined state or error handled by the fallback. The most likely cause is the `is_framed_object_strict` function being too restrictive, failing to recognize the magenta cross within the yellow frame because its pixels might touch the inner boundary of the frame's bounding box, or the logic to check if all interior space is accounted for failed.
*   **Example 2 Failure:** The code produced a 4x4 grid (correct size for the 'not contained' case) but used the wrong color (yellow=4 instead of red=2). This implies it correctly determined the 'not contained' scenario but selected the wrong framed object based on the minimum `inner_color` rule. It likely selected an object with inner color 4 instead of the object with inner color 2. This could stem from incorrect identification of candidates by `is_framed_object_strict` or an error in the sorting/selection logic for the `not_contained` case.

**Strategy:**

1.  **Refine `is_framed_object_strict`:** Loosen the constraint that the inner object cannot touch the frame's bounding box edges. The crucial part is that it's a distinct contiguous object within the white space defined by the frame, and its color differs from the frame. Ensure the check for surrounding white space and the single inner object is robust.
2.  **Verify Container Identification:** Double-check that `find_largest_solid_block` correctly identifies the large red block in Example 1 and the large azure block in Example 2, applying tie-breaking rules correctly.
3.  **Verify Target Selection Logic:** Step through the selection process for both examples:
    *   Example 1: Confirm the single framed object is found, the red container is found, containment is true, and the 5x5 output is generated with the correct colors (inner=magenta=6, primary=red=2).
    *   Example 2: Confirm *all* framed objects are found (especially the one with inner=red=2 and others with inner=yellow=4). Confirm the azure container is found. Confirm containment check fails for the red-inner object. Confirm the sorting for the 'not contained' case correctly picks the object with inner=red=2 based on the minimum color rule. Confirm the 4x4 output is generated with primary=red=2.
4.  **Gather Metrics:** Use code execution to log the intermediate findings (identified objects, container, selected target, containment status) for each example to pinpoint the exact step where the logic deviates.

**Metrics Gathering**

