
## train_1

**input:**
```
0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 2 2 0 0 0 0 0 0 0 2 2 0 0 0
0 0 2 2 2 2 0 0 0 0 0 2 2 2 2 0 0
0 2 2 2 2 2 2 0 0 0 2 2 2 2 2 2 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 3 0 0 0 3 0 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 3 0 0 0 3 0 3 0 0 0 3 0
0 0 3 0 3 0 0 0 3 0 3 0 0
0 0 0 3 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception**

*   **Input/Output Structure:** Both examples show input and output grids of the same dimensions. The grids contain a white background (0) and several distinct colored objects.
*   **Objects and Colors:**
    *   Example 1: Contains one red (2) object and two blue (1) objects.
    *   Example 2: Contains two yellow (4) objects and one green (3) object.
*   **Transformation:**
    *   In both examples, there are two objects of one color (blue in Ex1, yellow in Ex2) and one object of another color (red in Ex1, green in Ex2).
    *   The pair of objects (blue/yellow) remain unchanged in their positions from input to output.
    *   The single object (red/green) is copied. The original single object remains in place, and a duplicate appears in the output grid.
    *   The position of the duplicated object seems related to the pair of objects. In Ex1, the original red object is near the top-left blue object. The duplicated red object appears near the top-right blue object, in a similar relative position (above it).
    *   In Ex2, the original green object is below the left yellow object. The duplicated green object appears below the right yellow object, again in a similar relative position.
*   **Spatial Relationship:** The core transformation appears to be identifying a pair of 'anchor' objects and a single 'mobile' object. The relative spatial relationship (e.g., offset vector) between the mobile object and the first anchor object is determined. This same relationship is then applied to the second anchor object to find the position for the *copy* of the mobile object.

**Facts**


```yaml
task_description: Copy a specific object based on its relationship to a pair of identical anchor objects.

examples:
  - id: train_1
    input_grid_size: [10, 17]
    output_grid_size: [10, 17]
    objects:
      - color: red
        count: 1
        role: mobile
        location_relation: Above the first blue object.
      - color: blue
        count: 2
        role: anchor
        description: Rectangular shapes.
    transformation:
      action: copy
      source_object_color: red
      target_location_rule: Maintain the same relative position (above) with respect to the second blue anchor object as the original red object has to the first blue anchor object.

  - id: train_2
    input_grid_size: [11, 13]
    output_grid_size: [11, 13]
    objects:
      - color: green
        count: 1
        role: mobile
        location_relation: Below the first yellow object.
      - color: yellow
        count: 2
        role: anchor
        description: Shapes resembling the number 8.
    transformation:
      action: copy
      source_object_color: green
      target_location_rule: Maintain the same relative position (below) with respect to the second yellow anchor object as the original green object has to the first yellow anchor object.

general_rules:
  - Find all distinct objects (contiguous non-white pixels).
  - Identify the color with exactly two objects (anchor color).
  - Identify the color with exactly one object (mobile color).
  - Determine the 'first' and 'second' anchor objects (e.g., by top-left coordinate).
  - Calculate the positional offset (vector) from the top-left corner of the first anchor object to the top-left corner of the mobile object.
  - Calculate the target position for the copy by adding this offset to the top-left corner of the second anchor object.
  - Copy the pixel pattern of the mobile object to the target position in the output grid.
  - All other pixels remain unchanged from the input.
```


**Natural Language Program**

1.  **Identify Objects:** Scan the input grid to find all contiguous blocks of pixels with the same non-white color. Record each object's color, pixels, and bounding box.
2.  **Categorize Objects:** Group the identified objects by color and count how many objects exist for each color.
3.  **Find Anchor Pair:** Identify the color that has exactly two objects. These are the 'anchor' objects.
4.  **Find Mobile Object:** Identify the color that has exactly one object. This is the 'mobile' object.
5.  **Order Anchors:** Determine which anchor object is the 'first' (e.g., the one whose bounding box's top-left corner has the smallest row index, breaking ties with the smallest column index). Label this `Anchor1` and the other `Anchor2`.
6.  **Calculate Offset:** Compute the vector difference (delta_row, delta_col) between the top-left corner coordinates of the mobile object's bounding box and the top-left corner coordinates of `Anchor1`'s bounding box. `offset = mobile_top_left - anchor1_top_left`.
7.  **Determine Copy Position:** Calculate the target top-left corner coordinates for the copied mobile object by adding the calculated offset to the top-left corner coordinates of `Anchor2`'s bounding box. `copy_target_top_left = anchor2_top_left + offset`.
8.  **Generate Output:** Create a copy of the input grid. Iterate through the pixels of the original mobile object relative to its own top-left corner. For each pixel, calculate its corresponding position relative to the `copy_target_top_left` and place the mobile object's color at that coordinate in the copied grid. The final copied grid is the output.
```python
"""
Identify objects by color. Find the color with exactly two objects (anchors) and the color with exactly one object (mobile). Determine the spatial offset between the first anchor (top-leftmost) and the mobile object. Apply this same offset to the second anchor to find the target location. Copy the mobile object to the target location in the output grid, leaving the rest of the input grid unchanged.
"""

import numpy as np
from collections import defaultdict

def find_objects(grid):
    """
    Finds all contiguous objects of the same color in the grid.
    
    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each representing an object with keys:
              'color' (int): The color of the object.
              'pixels' (set): A set of (row, col) tuples for the object's pixels.
              'bbox' (tuple): The bounding box (min_row, min_col, max_row, max_col).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0: # 0 is background
                color = grid[r, c]
                obj_pixels = set()
                q = [(r, c)]
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.pop(0)
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

def transform(input_grid):
    """
    Applies the transformation rule: Copy a single object based on its relative
    position to a pair of anchor objects.

    Args:
        input_grid (np.ndarray): The input 2D array representing the grid.

    Returns:
        np.ndarray: The transformed 2D array.
    """
    
    # 1. Find all objects in the input grid
    objects = find_objects(input_grid)

    # 2. Categorize objects by color and count them
    objects_by_color = defaultdict(list)
    for obj in objects:
        objects_by_color[obj['color']].append(obj)

    anchor_color = None
    mobile_color = None
    anchor_objects = []
    mobile_object = None

    # 3. Find Anchor Pair and Mobile Object
    for color, obj_list in objects_by_color.items():
        if len(obj_list) == 2:
            anchor_color = color
            anchor_objects = obj_list
        elif len(obj_list) == 1:
            mobile_color = color
            mobile_object = obj_list[0]

    # Check if we found the required objects
    if anchor_color is None or mobile_color is None:
        # If the pattern doesn't match (e.g., different counts), return the input unchanged
        # or handle as an error, depending on desired behavior. 
        # For now, return a copy of the input.
        return np.copy(input_grid) 

    # 4. Order Anchors (Anchor1 is top-leftmost)
    anchor1 = min(anchor_objects, key=lambda obj: (obj['bbox'][0], obj['bbox'][1]))
    anchor2 = max(anchor_objects, key=lambda obj: (obj['bbox'][0], obj['bbox'][1]))

    # 5. Calculate Offset
    mob_r0, mob_c0, _, _ = mobile_object['bbox']
    anc1_r0, anc1_c0, _, _ = anchor1['bbox']
    delta_row = mob_r0 - anc1_r0
    delta_col = mob_c0 - anc1_c0

    # 6. Determine Copy Position
    anc2_r0, anc2_c0, _, _ = anchor2['bbox']
    copy_target_r0 = anc2_r0 + delta_row
    copy_target_c0 = anc2_c0 + delta_col
    
    # 7. Generate Output: Start with a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 8. Copy the mobile object's pixels to the target location
    mobile_color = mobile_object['color']
    for r_pix, c_pix in mobile_object['pixels']:
        # Calculate pixel position relative to the mobile object's top-left
        relative_r = r_pix - mob_r0
        relative_c = c_pix - mob_c0
        
        # Calculate the target pixel position in the output grid
        target_r = copy_target_r0 + relative_r
        target_c = copy_target_c0 + relative_c

        # Ensure the target position is within bounds before drawing
        if 0 <= target_r < rows and 0 <= target_c < cols:
            output_grid[target_r, target_c] = mobile_color

    return output_grid
```

Previous Code:
```python
"""
Identify objects by color. Find the color with exactly two objects (anchors) and the color with exactly one object (mobile). Determine the spatial offset between the first anchor (top-leftmost) and the mobile object. Apply this same offset to the second anchor to find the target location. Copy the mobile object to the target location in the output grid, leaving the rest of the input grid unchanged.
"""

import numpy as np
from collections import defaultdict

def find_objects(grid):
    """
    Finds all contiguous objects of the same color in the grid.
    
    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each representing an object with keys:
              'color' (int): The color of the object.
              'pixels' (set): A set of (row, col) tuples for the object's pixels.
              'bbox' (tuple): The bounding box (min_row, min_col, max_row, max_col).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0: # 0 is background
                color = grid[r, c]
                obj_pixels = set()
                q = [(r, c)]
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.pop(0)
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

def transform(input_grid):
    """
    Applies the transformation rule: Copy a single object based on its relative
    position to a pair of anchor objects.

    Args:
        input_grid (np.ndarray): The input 2D array representing the grid.

    Returns:
        np.ndarray: The transformed 2D array.
    """
    
    # 1. Find all objects in the input grid
    objects = find_objects(input_grid)

    # 2. Categorize objects by color and count them
    objects_by_color = defaultdict(list)
    for obj in objects:
        objects_by_color[obj['color']].append(obj)

    anchor_color = None
    mobile_color = None
    anchor_objects = []
    mobile_object = None

    # 3. Find Anchor Pair and Mobile Object
    for color, obj_list in objects_by_color.items():
        if len(obj_list) == 2:
            anchor_color = color
            anchor_objects = obj_list
        elif len(obj_list) == 1:
            mobile_color = color
            mobile_object = obj_list[0]

    # Check if we found the required objects
    if anchor_color is None or mobile_color is None:
        # If the pattern doesn't match (e.g., different counts), return the input unchanged
        # or handle as an error, depending on desired behavior. 
        # For now, return a copy of the input.
        return np.copy(input_grid) 

    # 4. Order Anchors (Anchor1 is top-leftmost)
    anchor1 = min(anchor_objects, key=lambda obj: (obj['bbox'][0], obj['bbox'][1]))
    anchor2 = max(anchor_objects, key=lambda obj: (obj['bbox'][0], obj['bbox'][1]))

    # 5. Calculate Offset
    mob_r0, mob_c0, _, _ = mobile_object['bbox']
    anc1_r0, anc1_c0, _, _ = anchor1['bbox']
    delta_row = mob_r0 - anc1_r0
    delta_col = mob_c0 - anc1_c0

    # 6. Determine Copy Position
    anc2_r0, anc2_c0, _, _ = anchor2['bbox']
    copy_target_r0 = anc2_r0 + delta_row
    copy_target_c0 = anc2_c0 + delta_col
    
    # 7. Generate Output: Start with a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 8. Copy the mobile object's pixels to the target location
    mobile_color = mobile_object['color']
    for r_pix, c_pix in mobile_object['pixels']:
        # Calculate pixel position relative to the mobile object's top-left
        relative_r = r_pix - mob_r0
        relative_c = c_pix - mob_c0
        
        # Calculate the target pixel position in the output grid
        target_r = copy_target_r0 + relative_r
        target_c = copy_target_c0 + relative_c

        # Ensure the target position is within bounds before drawing
        if 0 <= target_r < rows and 0 <= target_c < cols:
            output_grid[target_r, target_c] = mobile_color

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 2 2 0 0 0 0 0 0 0 2 2 0 0 0
0 0 2 2 2 2 0 0 0 0 0 2 2 2 2 0 0
0 2 2 2 2 2 2 0 0 0 2 2 2 2 2 2 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 2 2 0 0 0 0 0 0 0 2 2 0 0 0
0 0 2 2 2 2 0 0 0 0 0 2 2 2 2 0 0
0 2 2 2 2 2 2 0 0 0 2 2 2 2 2 2 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 2:
Input:
```
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 3 0 0 0 3 0 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 3 0 0 0 3 0 3 0 0 0 3 0
0 0 3 0 3 0 0 0 3 0 3 0 0
0 0 0 3 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 3 0 0 0 3 0 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 6.993006993006986
**General Assessment**

The initial analysis correctly identified the core pattern of copying one object based on its relative position to a pair of anchor objects. The code implemented this logic successfully for `train_1`. However, the failure on `train_2` revealed an incorrect assumption about the definition of the "mobile object". The initial code assumed the mobile object must be a single, contiguous block of pixels. Example `train_2` shows that the "mobile object" can be a collection of disconnected pixels of the same color, which are treated as a single entity for the copy operation.

The strategy needs refinement to handle potentially disconnected pixels for the mobile object. The anchor objects still appear to be single, contiguous blocks.

**Metrics Gathering**

Let's gather metrics for the objects based on the *revised* understanding. We need to identify the anchor color (2 contiguous objects) and the mobile color (all pixels of another color treated as one object).



*code_execution:*
```python
import numpy as np
from collections import defaultdict

def find_objects(grid):
    """Finds contiguous objects (4-connectivity)."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                color = grid[r, c]
                obj_pixels = set()
                q = [(r, c)]
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                while q:
                    row, col = q.pop(0)
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c),
                    'top_left': (min_r, min_c)
                })
    return objects

def get_color_pixel_groups(grid):
    """Groups all pixels by color and finds their overall bounding box."""
    pixels_by_color = defaultdict(set)
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r,c]
            if color != 0:
                pixels_by_color[color].add((r,c))

    groups = {}
    for color, pixels in pixels_by_color.items():
        if not pixels: continue
        min_r = min(r for r, c in pixels)
        min_c = min(c for r, c in pixels)
        max_r = max(r for r, c in pixels)
        max_c = max(c for r, c in pixels)
        groups[color] = {
            'color': color,
            'pixels': pixels,
            'bbox': (min_r, min_c, max_r, max_c),
            'top_left': (min_r, min_c),
            'pixel_count': len(pixels)
        }
    return groups

# Example 1 Data
grid1_in = np.array([
    [0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0],
    [0,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
])

# Example 2 Data
grid2_in = np.array([
    [0,4,4,4,4,4,0,4,4,4,4,4,0],
    [0,4,0,0,0,4,0,4,0,0,0,4,0],
    [0,4,0,0,0,4,0,4,0,0,0,4,0],
    [0,4,4,4,4,4,0,4,4,4,4,4,0],
    [0,4,0,0,0,4,0,4,0,0,0,4,0],
    [0,4,0,0,0,4,0,4,0,0,0,4,0],
    [0,4,4,4,4,4,0,4,4,4,4,4,0],
    [0,3,0,0,0,3,0,0,0,0,0,0,0],
    [0,0,3,0,3,0,0,0,0,0,0,0,0],
    [0,0,0,3,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0]
])

# Analyze Example 1
print("--- Example 1 Analysis ---")
objects1 = find_objects(grid1_in)
objects_by_color1 = defaultdict(list)
for obj in objects1:
    objects_by_color1[obj['color']].append(obj)

anchor_color1 = None
mobile_color1 = None
anchor_objects1 = []
mobile_pixels1 = None

for color, obj_list in objects_by_color1.items():
    if len(obj_list) == 2:
        anchor_color1 = color
        anchor_objects1 = sorted(obj_list, key=lambda x: x['top_left']) # Sort by top-left
    # Mobile object in ex1 is contiguous, so this works, but we'll use the new logic
    # elif len(obj_list) == 1:
    #     mobile_color1 = color

# Identify mobile color using pixel groups
groups1 = get_color_pixel_groups(grid1_in)
for color, group_data in groups1.items():
    if color != anchor_color1:
        mobile_color1 = color
        mobile_pixels1 = group_data['pixels']
        mobile_bbox1 = group_data['bbox']
        mobile_top_left1 = group_data['top_left']
        break # Assume only one other color

print(f"Anchor Color: {anchor_color1}")
print(f"Anchor Object 1 Top-Left: {anchor_objects1[0]['top_left']}")
print(f"Anchor Object 2 Top-Left: {anchor_objects1[1]['top_left']}")
print(f"Mobile Color: {mobile_color1}")
print(f"Mobile Pixel Count: {len(mobile_pixels1)}")
print(f"Mobile Bounding Box Top-Left: {mobile_top_left1}")
offset1_row = mobile_top_left1[0] - anchor_objects1[0]['top_left'][0]
offset1_col = mobile_top_left1[1] - anchor_objects1[0]['top_left'][1]
print(f"Calculated Offset (Row, Col): ({offset1_row}, {offset1_col})")
target1_row = anchor_objects1[1]['top_left'][0] + offset1_row
target1_col = anchor_objects1[1]['top_left'][1] + offset1_col
print(f"Target Top-Left for Copy: ({target1_row}, {target1_col})")

# Analyze Example 2
print("\n--- Example 2 Analysis ---")
objects2 = find_objects(grid2_in)
objects_by_color2 = defaultdict(list)
for obj in objects2:
    objects_by_color2[obj['color']].append(obj)

anchor_color2 = None
mobile_color2 = None
anchor_objects2 = []
mobile_pixels2 = None

for color, obj_list in objects_by_color2.items():
    if len(obj_list) == 2:
        anchor_color2 = color
        anchor_objects2 = sorted(obj_list, key=lambda x: x['top_left']) # Sort by top-left

# Identify mobile color using pixel groups
groups2 = get_color_pixel_groups(grid2_in)
for color, group_data in groups2.items():
    if color != anchor_color2:
        mobile_color2 = color
        mobile_pixels2 = group_data['pixels']
        mobile_bbox2 = group_data['bbox']
        mobile_top_left2 = group_data['top_left']
        break # Assume only one other color

print(f"Anchor Color: {anchor_color2}")
print(f"Anchor Object 1 Top-Left: {anchor_objects2[0]['top_left']}")
print(f"Anchor Object 2 Top-Left: {anchor_objects2[1]['top_left']}")
print(f"Mobile Color: {mobile_color2}")
print(f"Mobile Pixel Count: {len(mobile_pixels2)}")
print(f"Mobile Bounding Box Top-Left: {mobile_top_left2}")
offset2_row = mobile_top_left2[0] - anchor_objects2[0]['top_left'][0]
offset2_col = mobile_top_left2[1] - anchor_objects2[0]['top_left'][1]
print(f"Calculated Offset (Row, Col): ({offset2_row}, {offset2_col})")
target2_row = anchor_objects2[1]['top_left'][0] + offset2_row
target2_col = anchor_objects2[1]['top_left'][1] + offset2_col
print(f"Target Top-Left for Copy: ({target2_row}, {target2_col})")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 1 Analysis ---
Anchor Color: 1
Anchor Object 1 Top-Left: (3, 1)
Anchor Object 2 Top-Left: (3, 10)
Mobile Color: 2
Mobile Pixel Count: 12
Mobile Bounding Box Top-Left: (0, 1)
Calculated Offset (Row, Col): (-3, 0)
Target Top-Left for Copy: (0, 10)

--- Example 2 Analysis ---
Anchor Color: 4
Anchor Object 1 Top-Left: (0, 1)
Anchor Object 2 Top-Left: (0, 7)
Mobile Color: 3
Mobile Pixel Count: 5
Mobile Bounding Box Top-Left: (7, 1)
Calculated Offset (Row, Col): (7, 0)
Target Top-Left for Copy: (7, 7)

```
**Facts**


```yaml
task_description: Copy a set of pixels ('mobile object') based on its positional relationship to a pair of identical 'anchor objects'.

definitions:
  anchor_objects: Two distinct, contiguous objects of the same color.
  mobile_object: The complete set of all pixels of a different, single color (these pixels may or may not be contiguous).
  bounding_box: The smallest rectangle enclosing a set of pixels.
  top_left_corner: The (row, column) coordinate of the top-leftmost pixel of a bounding box.

examples:
  - id: train_1
    input_grid_size: [10, 17]
    output_grid_size: [10, 17]
    anchor_objects:
      color: blue (1)
      count: 2
      top_left_corners: [(3, 1), (3, 10)]
    mobile_object:
      color: red (2)
      pixel_count: 12
      bounding_box_top_left: (0, 1) # Note: Bbox includes pixels (0,3), (0,4), (1,2) etc.
    relationship:
      offset_vector: (mobile_bbox_top_left - anchor1_bbox_top_left) = (0, 1) - (3, 1) = (-3, 0)
    transformation:
      action: copy
      source_object_color: red
      target_location_rule: Add offset (-3, 0) to anchor2_bbox_top_left (3, 10) -> Target top-left = (0, 10). Copy all red pixels relative to this new top-left.

  - id: train_2
    input_grid_size: [11, 13]
    output_grid_size: [11, 13]
    anchor_objects:
      color: yellow (4)
      count: 2
      top_left_corners: [(0, 1), (0, 7)]
    mobile_object:
      color: green (3)
      pixel_count: 5
      pixels_are_contiguous: false
      bounding_box_top_left: (7, 1) # Bbox includes pixels (7,1), (7,5), (8,2), (8,4), (9,3)
    relationship:
      offset_vector: (mobile_bbox_top_left - anchor1_bbox_top_left) = (7, 1) - (0, 1) = (7, 0)
    transformation:
      action: copy
      source_object_color: green
      target_location_rule: Add offset (7, 0) to anchor2_bbox_top_left (0, 7) -> Target top-left = (7, 7). Copy all green pixels relative to this new top-left.

general_rules:
  - Find all distinct contiguous objects using 4-connectivity.
  - Group these contiguous objects by color. Identify the color that has exactly two objects ('anchor_color').
  - Find all unique non-background colors present in the grid. Identify the color that is not the 'anchor_color' ('mobile_color'). Assume there is only one such color.
  - Collect all pixels in the grid that have the 'mobile_color'. This set constitutes the 'mobile_object'.
  - Determine the overall bounding box for all pixels of the 'mobile_object' and find its top-left corner ('mobile_bbox_top_left').
  - Identify the two anchor objects. Determine which is 'Anchor1' (e.g., the one whose bounding box top-left corner is top-leftmost) and 'Anchor2'. Get their bounding box top-left corners ('anchor1_bbox_top_left', 'anchor2_bbox_top_left').
  - Calculate the offset vector: `offset = mobile_bbox_top_left - anchor1_bbox_top_left`.
  - Calculate the target top-left corner for the copy: `copy_target_bbox_top_left = anchor2_bbox_top_left + offset`.
  - Create a copy of the input grid. For each pixel belonging to the 'mobile_object', calculate its position relative to 'mobile_bbox_top_left'. Add this relative position to 'copy_target_bbox_top_left' to get the final target coordinate in the output grid. Place the 'mobile_color' at this target coordinate.
  - All other pixels (background and anchor objects) remain unchanged from the input grid.
```


**Natural Language Program**

1.  **Identify Contiguous Objects:** Scan the input grid to find all separate contiguous blocks of same-colored, non-white pixels using 4-way adjacency. Record each block's color, pixels, and bounding box.
2.  **Find Anchor Color:** Group the identified contiguous objects by color. Find the color that corresponds to exactly two distinct contiguous objects. This is the `anchor_color`.
3.  **Identify Anchor Objects:** Label the two objects with the `anchor_color` as `anchor_objects`. Determine which is `Anchor1` (e.g., top-leftmost bounding box) and which is `Anchor2`. Record the top-left corner coordinates of their respective bounding boxes (`anchor1_top_left`, `anchor2_top_left`).
4.  **Find Mobile Color:** Identify all unique non-white colors present in the input grid. The color that is *not* the `anchor_color` is the `mobile_color`. (Assume only one such color exists besides the anchor color).
5.  **Define Mobile Object Pixels:** Collect the coordinates of *all* pixels in the input grid that have the `mobile_color`. This set of coordinates represents the `mobile_object`, regardless of whether the pixels are connected.
6.  **Calculate Mobile Bounding Box:** Determine the smallest bounding box that encloses all pixels of the `mobile_object`. Record the top-left corner coordinates of this bounding box (`mobile_bbox_top_left`).
7.  **Calculate Offset:** Compute the vector difference (delta_row, delta_col) between `mobile_bbox_top_left` and `anchor1_top_left`. `offset = mobile_bbox_top_left - anchor1_top_left`.
8.  **Determine Copy Target Origin:** Calculate the target top-left corner for placing the copied object: `copy_target_origin = anchor2_top_left + offset`.
9.  **Generate Output:** Create a copy of the input grid. Iterate through each pixel coordinate (`r_mob`, `c_mob`) belonging to the `mobile_object`. Calculate its position relative to the mobile object's bounding box origin: `relative_pos = (r_mob - mobile_bbox_top_left[0], c_mob - mobile_bbox_top_left[1])`. Calculate the final target coordinate in the output grid: `target_pos = copy_target_origin + relative_pos`. Place the `mobile_color` at `target_pos` in the copied grid, ensuring it's within grid bounds. The resulting grid is the output.
