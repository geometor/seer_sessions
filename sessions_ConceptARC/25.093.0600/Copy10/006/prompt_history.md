
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

Okay, let's break down the transformation logic for these examples.

**Perception of Elements:**

1.  **Grid Structure:** Both input and output are 2D grids of integers. The integer '0' represents the background color. Non-zero integers represent different foreground colors/parts of objects.
2.  **Objects:** The non-zero cells form distinct shapes or objects within the grid.
3.  **Object Composition:** Some objects appear nested; one shape (defined by one color) surrounds or encloses another shape (defined by a different color). For example, in `train_1`, the shape made of '3's encloses the shape made of '2's. In `train_2`, the '4's enclose the '1's.
4.  **Isolated Objects:** Inputs can contain multiple separate objects. Some might be simple (one color), while others are composite (enclosing/enclosed).
5.  **Transformation:** The transformation identifies one specific composite object (the enclosing one) from the input, copies it entirely (including the enclosed parts), and places the copy adjacent to the original in the output grid. Other isolated objects present in the input are discarded in the output.
6.  **Copy Placement:** The placement of the copy (either to the right or below the original) and the size of the gap (number of zero rows/columns) between the original and the copy seem dependent on the properties of the selected object.

**YAML Fact Document:**


```yaml
task_name: object_duplication_with_contextual_placement
description: Identify a specific composite object (one shape enclosing another) in the input grid, duplicate it, and place the copy adjacent to the original based on object properties. Discard other objects.

elements:
  - element: grid
    description: A 2D array of integers representing pixels.
    properties:
      - background_color: 0
      - foreground_colors: non-zero integers

  - element: object
    description: A connected component of non-zero cells.
    properties:
      - colors: list of unique non-zero integers within the object
      - bounding_box: coordinates of the minimum rectangle containing the object
      - width: width of the bounding box
      - height: height of the bounding box
      - type: simple (one color) or composite (enclosing/enclosed)

relationships:
  - relationship: encloses
    description: An object A encloses object B if B is fully contained within the bounding box of A, and A's cells form a boundary around B. Object A and B must have different primary colors.
    domain: object (composite, outer)
    range: object (inner)

actions:
  - action: identify_target_object
    description: Select the unique object from the input grid that encloses another object.
    input: input_grid
    output: target_object

  - action: determine_inner_color
    description: Find the primary color of the object enclosed by the target_object.
    input: target_object
    output: inner_color

  - action: calculate_gap
    description: The gap size between the original and copied object is equal to the inner_color.
    input: inner_color
    output: gap_size

  - action: determine_placement
    description: Decide placement direction (right or below) and calculate copy position based on target_object dimensions (width W, height H) and gap_size.
    input:
      - target_object (bounding box: r1, c1, r2, c2)
      - width (W)
      - height (H)
      - gap_size
    output:
      - placement_direction ('right' or 'below')
      - copy_top_left_corner (r_copy, c_copy)
    logic: |
      If H > W:
        placement_direction = 'below'
        copy_top_left_corner = (r2 + 1 + gap_size, c1)
      Else (W >= H):
        placement_direction = 'right'
        copy_top_left_corner = (r1, c2 + 1 + gap_size)

  - action: copy_object
    description: Extract the subgrid corresponding to the target_object's bounding box.
    input:
      - input_grid
      - target_object (bounding box)
    output: object_pattern (subgrid)

  - action: construct_output
    description: Create the output grid by placing the object_pattern copy into the input grid structure at the calculated position. Discard non-target objects from the input.
    input:
      - input_grid (containing only the target object and background)
      - object_pattern
      - copy_top_left_corner
    output: output_grid

```


**Natural Language Program:**

1.  Parse the input grid to identify all distinct connected objects formed by non-zero cells.
2.  Identify the specific "target" object which consists of an outer shape of one color enclosing an inner shape of a different color. Disregard any other objects in the input grid.
3.  Determine the bounding box of this target object (the smallest rectangle enclosing all its cells). Note its dimensions: width (W) and height (H).
4.  Identify the color of the *inner*, enclosed shape within the target object. Let this color value be `inner_color`.
5.  Calculate the gap size to be used between the original object and its copy: `gap = inner_color`.
6.  Determine the placement direction for the copy:
    *   If the target object's height (H) is greater than its width (W), the copy will be placed *below* the original.
    *   Otherwise (if width W is greater than or equal to height H), the copy will be placed to the *right* of the original.
7.  Calculate the top-left coordinate for placing the copy:
    *   If placing below: `copy_row = original_bottom_row + 1 + gap`, `copy_col = original_left_col`.
    *   If placing right: `copy_row = original_top_row`, `copy_col = original_right_col + 1 + gap`.
8.  Create the output grid, initially containing only the identified target object from the input grid (all other input objects are removed, replaced by the background color 0).
9.  Copy the pattern of the target object (defined by its bounding box) and paste this pattern into the output grid starting at the calculated top-left coordinate for the copy.
```python
import numpy as np
from collections import deque

"""
Identifies a composite object (an outer shape enclosing an inner shape of a different color) in the input grid.
Duplicates this object and places the copy adjacent to the original.
The gap between the original and the copy is determined by the color of the inner shape.
The placement direction (right or below) depends on the object's aspect ratio (width vs. height).
All other objects in the input are discarded. The output grid size is adjusted to fit the original and the copy.

Workflow:
1. Find all connected components (objects) of non-zero cells in the input grid.
2. Identify the 'target' object: the one whose bounding box contains exactly two distinct non-zero colors.
3. Determine the properties of the target object: bounding box, width, height, and the two colors.
4. Identify the 'inner' color (the minimum of the two non-zero colors).
5. Calculate the gap size between the original and copy (gap = inner_color).
6. Determine the placement direction: 'right' if width >= height, 'below' otherwise.
7. Calculate the top-left coordinates for the copied object based on direction and gap.
8. Extract the pattern (subgrid) of the target object from the input.
9. Determine the required dimensions for the output grid to hold the original and the copy.
10. Create the output grid, initialized with zeros.
11. Place the original object pattern into the output grid.
12. Place the copied object pattern into the output grid at the calculated position.
13. Return the output grid.
"""

def find_connected_components(grid):
    """Finds all connected components of non-zero cells."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                component_cells = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component_cells.add((r, c))

                while q:
                    row, col = q.popleft()
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            component_cells.add((nr, nc))
                components.append(component_cells)
    return components

def get_bounding_box(component_cells):
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a component."""
    if not component_cells:
        return None
    min_r = min(r for r, c in component_cells)
    min_c = min(c for r, c in component_cells)
    max_r = max(r for r, c in component_cells)
    max_c = max(c for r, c in component_cells)
    return min_r, min_c, max_r, max_c

def transform(input_grid_list):
    """
    Transforms the input grid according to the specified object duplication rule.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape

    # 1. Find all connected components
    components = find_connected_components(input_grid)

    target_object_info = None

    # 2. Identify the 'target' object
    for component in components:
        if not component: continue
        bbox = get_bounding_box(component)
        if bbox is None: continue
        r1, c1, r2, c2 = bbox
        
        # Extract subgrid based on bounding box
        subgrid = input_grid[r1:r2+1, c1:c2+1]
        
        # Find unique non-zero colors within the *bounding box*
        unique_colors_in_bbox = set(subgrid[subgrid != 0].flatten())

        # Target object has exactly two distinct non-zero colors in its bounding box
        if len(unique_colors_in_bbox) == 2:
             width = c2 - c1 + 1
             height = r2 - r1 + 1
             target_object_info = {
                 'bbox': bbox,
                 'colors': list(unique_colors_in_bbox),
                 'width': width,
                 'height': height
             }
             break # Assume only one such object

    if target_object_info is None:
        # Handle cases where no target object is found (e.g., return original or empty)
        # For this problem, examples suggest a target always exists.
        # If not, returning the original grid might be a safe default.
        print("Warning: No target object found.")
        return input_grid_list 

    # 3. Determine properties of the target object
    bbox = target_object_info['bbox']
    colors = target_object_info['colors']
    width = target_object_info['width']
    height = target_object_info['height']
    r1, c1, r2, c2 = bbox

    # 4. Identify the 'inner' color (minimum of the two non-zero colors)
    inner_color = min(colors)

    # 5. Calculate the gap size
    gap = inner_color

    # 6. Determine placement direction
    if height > width:
        placement_direction = 'below'
    else: # width >= height
        placement_direction = 'right'

    # 7. Calculate the top-left coordinates for the copy
    if placement_direction == 'below':
        r_copy = r2 + 1 + gap
        c_copy = c1
        # 9. Determine the required dimensions for the output grid
        out_rows = r_copy + height
        out_cols = max(cols, c1 + width) # Ensure width accommodates original
    else: # placement_direction == 'right'
        r_copy = r1
        c_copy = c2 + 1 + gap
        # 9. Determine the required dimensions for the output grid
        out_rows = max(rows, r1 + height) # Ensure height accommodates original
        out_cols = c_copy + width

    # 8. Extract the pattern (subgrid) of the target object
    object_pattern = input_grid[r1:r2+1, c1:c2+1]

    # 10. Create the output grid, initialized with zeros
    output_grid = np.zeros((out_rows, out_cols), dtype=int)

    # 11. Place the original object pattern into the output grid
    output_grid[r1:r1+height, c1:c1+width] = object_pattern

    # 12. Place the copied object pattern into the output grid
    output_grid[r_copy:r_copy+height, c_copy:c_copy+width] = object_pattern

    # Convert back to list of lists for the required output format
    return output_grid.tolist()
```
```python
import numpy as np
from collections import deque

"""
Identifies a composite object (an outer shape enclosing an inner shape of a different color) in the input grid.
Duplicates this object and places the copy adjacent to the original.
The gap between the original and the copy is determined by the color value of the inner shape (the minimum of the two colors).
The placement direction (right or below) depends on the object's bounding box aspect ratio (width vs. height).
All other objects in the input are discarded. The output grid size is determined by the space needed to contain the original and copied object.

Workflow:
1. Find all connected components (objects) of non-zero cells.
2. Identify the 'target' object: the one whose bounding box contains exactly two distinct non-zero colors.
3. Extract properties: bounding box (r1, c1, r2, c2), width (W), height (H), the two colors.
4. Extract the object pattern (subgrid) from the input based on the bounding box.
5. Identify the 'inner' color as the minimum of the two colors.
6. Calculate the gap size: gap = inner_color.
7. Determine placement direction: 'below' if H > W, 'right' otherwise.
8. Calculate the top-left coordinates (copy_r, copy_c) for the copied object based on direction and gap.
9. Calculate the required dimensions for the output grid (out_rows, out_cols) to hold the original and the copy.
10. Create the output grid, initialized with zeros.
11. Place the original object pattern into the output grid at its original relative position (r1, c1).
12. Place the copied object pattern into the output grid at the calculated position (copy_r, copy_c).
13. Return the output grid as a list of lists.
"""

def find_connected_components(grid):
    """Finds all connected components of non-zero cells using BFS."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                component_cells = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component_cells.add((r, c))
                component_colors = {grid[r,c]}

                while q:
                    row, col = q.popleft()
                    component_colors.add(grid[row, col])
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            component_cells.add((nr, nc))
                
                # Store component cells and their colors
                components.append({'cells': component_cells, 'colors': component_colors})
    return components

def get_bounding_box(component_cells):
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a set of cells."""
    if not component_cells:
        return None
    min_r = min(r for r, c in component_cells)
    min_c = min(c for r, c in component_cells)
    max_r = max(r for r, c in component_cells)
    max_c = max(c for r, c in component_cells)
    return min_r, min_c, max_r, max_c

def transform(input_grid_list):
    """
    Transforms the input grid according to the specified object duplication rule.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape

    # 1. Find all connected components
    components = find_connected_components(input_grid)

    target_object_info = None

    # 2. Identify the 'target' object
    for component_data in components:
        cells = component_data['cells']
        if not cells: continue
        
        # Calculate bounding box for the component itself
        comp_bbox = get_bounding_box(cells)
        if comp_bbox is None: continue
        r1_comp, c1_comp, r2_comp, c2_comp = comp_bbox

        # Extract subgrid based on the component's bounding box
        subgrid = input_grid[r1_comp:r2_comp+1, c1_comp:c2_comp+1]

        # Find unique non-zero colors *within the component's bounding box*
        unique_colors_in_bbox = set(np.unique(subgrid[subgrid != 0]))

        # Target object has exactly two distinct non-zero colors in its bounding box
        if len(unique_colors_in_bbox) == 2:
            width = r2_comp - r1_comp + 1
            height = c2_comp - c1_comp + 1
            # IMPORTANT: The original code swapped width and height calculation. Fixing it.
            height = r2_comp - r1_comp + 1
            width = c2_comp - c1_comp + 1
            
            target_object_info = {
                 'bbox': comp_bbox,
                 'colors': list(unique_colors_in_bbox),
                 'width': width,
                 'height': height
             }
            break # Assume only one such object

    if target_object_info is None:
        # Handle cases where no target object is found (e.g., return original or empty)
        # Based on examples, we expect one target. If not, returning the input might be safest.
        # print("Warning: No target object found matching criteria.")
        return input_grid_list 

    # 3. Extract properties
    bbox = target_object_info['bbox']
    colors = target_object_info['colors']
    width = target_object_info['width']
    height = target_object_info['height']
    r1, c1, r2, c2 = bbox

    # 4. Extract the object pattern
    object_pattern = input_grid[r1:r2+1, c1:c2+1]

    # 5. Identify the 'inner' color (minimum of the two non-zero colors)
    inner_color = min(colors)

    # 6. Calculate the gap size
    gap = inner_color

    # 7. Determine placement direction
    if height > width:
        placement_direction = 'below'
    else: # width >= height
        placement_direction = 'right'

    # 8. Calculate the top-left coordinates for the copy
    if placement_direction == 'below':
        copy_r = r2 + 1 + gap
        copy_c = c1
        # 9. Determine the required dimensions for the output grid
        out_rows = copy_r + height
        out_cols = c1 + width # Width determined by original position + pattern width
    else: # placement_direction == 'right'
        copy_r = r1
        copy_c = c2 + 1 + gap
        # 9. Determine the required dimensions for the output grid
        out_rows = r1 + height # Height determined by original position + pattern height
        out_cols = copy_c + width

    # 10. Create the output grid, initialized with zeros
    # Ensure output grid is large enough, using calculated dimensions
    output_grid = np.zeros((out_rows, out_cols), dtype=int)

    # 11. Place the original object pattern into the output grid
    # Check bounds just in case, although calculation should be correct
    if r1+height <= out_rows and c1+width <= out_cols:
        output_grid[r1:r1+height, c1:c1+width] = object_pattern
    else:
        print(f"Warning: Original placement out of bounds: ({r1}:{r1+height}, {c1}:{c1+width}) vs ({out_rows}, {out_cols})")


    # 12. Place the copied object pattern into the output grid
    # Check bounds just in case
    if copy_r+height <= out_rows and copy_c+width <= out_cols:
         output_grid[copy_r:copy_r+height, copy_c:copy_c+width] = object_pattern
    else:
        print(f"Warning: Copy placement out of bounds: ({copy_r}:{copy_r+height}, {copy_c}:{copy_c+width}) vs ({out_rows}, {out_cols})")


    # 13. Return the output grid as a list of lists
    return output_grid.tolist()
```
```python
import numpy as np
from collections import deque
import copy

"""
Identifies a unique composite object in the input grid, characterized by an outer shape of one color (Co) enclosing an inner shape of a different color (Ci).
All other objects in the input are discarded.
This target object is duplicated, and the copy is placed adjacent to the original.
The placement direction (below or right) and the gap size between the original and the copy depend on the object's dimensions (Height H, Width W) and the values of the inner (Ci) and outer (Co) colors according to the following rules:

1.  **Placement Direction:**
    *   Place BELOW if Height (H) > Width (W) OR if the Outer Color (Co) is exactly twice the Inner Color (Ci) (Co == 2 * Ci).
    *   Otherwise, place RIGHT.

2.  **Gap Size:**
    *   If Inner Color (Ci) > Outer Color (Co), Gap = abs(Ci - Co).
    *   Else if Outer Color (Co) == 2 * Inner Color (Ci), Gap = Height (H).
    *   Otherwise (Ci <= Co and Co != 2 * Ci), Gap = Inner Color (Ci).

The output grid size is determined dynamically to accommodate both the original object in its input position and the placed copy.
"""

def find_connected_components(grid):
    """Finds all connected components of non-zero cells using BFS."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                component_cells = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component_cells.add((r, c))

                while q:
                    row, col = q.popleft()
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            component_cells.add((nr, nc))
                
                if component_cells:
                    components.append(component_cells)
    return components

def get_bounding_box(component_cells):
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a set of cells."""
    if not component_cells:
        return None
    min_r = min(r for r, c in component_cells)
    min_c = min(c for r, c in component_cells)
    max_r = max(r for r, c in component_cells)
    max_c = max(c for r, c in component_cells)
    return min_r, min_c, max_r, max_c

def identify_inner_outer_colors(subgrid):
    """Identifies the inner (Ci) and outer (Co) colors within a subgrid."""
    height, width = subgrid.shape
    colors = set(np.unique(subgrid[subgrid != 0]))
    if len(colors) != 2:
        return None, None # Should not happen for target object

    outer_color = None
    # Check boundary pixels of the subgrid
    boundary_pixels = []
    if height > 0:
        boundary_pixels.extend(subgrid[0, :].tolist()) # Top row
        boundary_pixels.extend(subgrid[height-1, :].tolist()) # Bottom row
    if width > 0:
        boundary_pixels.extend(subgrid[:, 0].tolist()) # Left col
        boundary_pixels.extend(subgrid[:, width-1].tolist()) # Right col
        
    for pixel_color in boundary_pixels:
        if pixel_color in colors:
            outer_color = pixel_color
            break

    if outer_color is None:
         # Fallback or error: If no boundary pixel has one of the two colors,
         # this indicates an issue or a very thin object.
         # Let's make an assumption or raise error. Assume the larger color is outer?
         # Or maybe the color covering more area? Let's stick to boundary for now.
         # If boundary doesn't work, maybe check corners?
         # A simpler assumption might be needed if boundary fails.
         # Let's assume the numerically larger color is outer if boundary fails.
         # print("Warning: Could not determine outer color from boundary pixels. Assuming numerically larger.")
         outer_color = max(colors)


    inner_color = (colors - {outer_color}).pop()
    return inner_color, outer_color


def transform(input_grid_list):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape

    # 1. Find all connected components
    components = find_connected_components(input_grid)

    target_object_info = None

    # 2. Identify the 'target' object (composite object with 2 colors)
    for component in components:
        if not component: continue
        
        bbox = get_bounding_box(component)
        if bbox is None: continue
        r1, c1, r2, c2 = bbox

        # Extract subgrid based on the component's bounding box
        subgrid = input_grid[r1:r2+1, c1:c2+1]

        # Find unique non-zero colors *within the component's bounding box*
        unique_colors_in_bbox = set(np.unique(subgrid[subgrid != 0]))

        # Target object has exactly two distinct non-zero colors in its bounding box
        if len(unique_colors_in_bbox) == 2:
            height = r2 - r1 + 1
            width = c2 - c1 + 1
            
            # 3. Identify Inner (Ci) and Outer (Co) colors
            Ci, Co = identify_inner_outer_colors(subgrid)
            if Ci is None or Co is None:
                continue # Skip if colors couldn't be determined

            target_object_info = {
                 'bbox': bbox,
                 'inner_color': Ci,
                 'outer_color': Co,
                 'width': width,
                 'height': height,
                 'pattern': subgrid
             }
            break # Assume only one such object per input

    if target_object_info is None:
        # If no target object found, return the input unchanged (as per some ARC tasks)
        # Or handle as an error, depending on expected behavior.
        # print("Warning: No target object found matching criteria.")
        return input_grid_list 

    # Extract properties for calculation
    bbox = target_object_info['bbox']
    Ci = target_object_info['inner_color']
    Co = target_object_info['outer_color']
    W = target_object_info['width']
    H = target_object_info['height']
    r1, c1, r2, c2 = bbox
    object_pattern = target_object_info['pattern']

    # 4. Determine Placement Direction
    place_below = (H > W) or (Co == 2 * Ci)

    # 5. Calculate Gap Size
    if Ci > Co:
        gap = abs(Ci - Co)
    elif Co == 2 * Ci:
        gap = H
    else: # Ci <= Co and Co != 2 * Ci
        gap = Ci

    # 6. Calculate Copy Position
    if place_below:
        placement_direction = 'below'
        copy_r = r2 + 1 + gap
        copy_c = c1
    else:
        placement_direction = 'right'
        copy_r = r1
        copy_c = c2 + 1 + gap

    # 7. Calculate Output Grid Size
    # Max row needed considers original position and copy position
    required_rows = max(r1 + H, copy_r + H)
    # Max col needed considers original position and copy position
    required_cols = max(c1 + W, copy_c + W)
    
    # Output grid should be at least as large as input, and large enough for content
    out_rows = max(rows, required_rows)
    out_cols = max(cols, required_cols)

    # 8. Construct Output Grid
    # Initialize with zeros (background color)
    output_grid = np.zeros((out_rows, out_cols), dtype=int)

    # Place the original target object pattern
    # Ensure slicing does not go out of bounds of the output grid
    orig_end_r = min(r1 + H, out_rows)
    orig_end_c = min(c1 + W, out_cols)
    output_grid[r1:orig_end_r, c1:orig_end_c] = object_pattern[:orig_end_r-r1, :orig_end_c-c1]

    # Place the copied target object pattern
    # Ensure slicing does not go out of bounds of the output grid
    copy_end_r = min(copy_r + H, out_rows)
    copy_end_c = min(copy_c + W, out_cols)
    output_grid[copy_r:copy_end_r, copy_c:copy_end_c] = object_pattern[:copy_end_r-copy_r, :copy_end_c-copy_c]

    # Convert back to list of lists for the required output format
    return output_grid.tolist()
```
