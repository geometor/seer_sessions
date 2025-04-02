
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 4 4 4 0 0 0 8
0 0 0 2 2 2 0 0 0 8
0 0 0 3 3 3 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided task examples.

## Perception

*   **`train_1` Example:**
    *   The input grid contains three horizontal lines (yellow, red, green), each 3 pixels wide, stacked vertically near the center. The background is white.
    *   The output grid is identical to the input, but with the addition of a solid azure vertical line filling the entire rightmost column.
    *   The primary input shapes are horizontal. The added feature is a vertical line on the right border. The color added (azure/8) is not present in the input colors (yellow/4, red/2, green/3).

*   **`train_2` Example:**
    *   The input grid contains a 4x4 block of colors (orange, azure, maroon, blue columns) roughly centered. The background is white.
    *   The output grid is identical to the input, but with the addition of a solid azure horizontal line filling the entire topmost row.
    *   The primary input shapes can be seen as vertical lines of distinct colors adjacent to each other. The added feature is a horizontal line on the top border. The color added (azure/8) *is* present in the input colors.

*   **Comparison & Pattern:**
    *   Both examples involve adding a single, solid-colored line to one of the grid's borders.
    *   The orientation of the added line seems opposite to the orientation of the primary shapes in the input (horizontal input shapes -> vertical output line; vertical input shapes -> horizontal output line).
    *   The position of the added line seems consistent based on the orientation: vertical lines are added to the rightmost column, and horizontal lines are added to the topmost row.
    *   The color of the added line is azure (8) in both cases. In `train_2`, azure is present in the input; in `train_1`, it is not. This suggests the added color might be consistently azure (8), regardless of input colors, but determined by the input shape orientation rule.

## Facts


```yaml
task_description: Add a single line of a specific color to one border of the grid, based on the orientation of shapes within the input grid.

examples:
  train_1:
    input:
      grid_size: [10, 10]
      background_color: white (0)
      objects:
        - shape: horizontal line
          color: yellow (4)
          location: rows=[4], cols=[3, 4, 5]
          size: [1, 3]
        - shape: horizontal line
          color: red (2)
          location: rows=[5], cols=[3, 4, 5]
          size: [1, 3]
        - shape: horizontal line
          color: green (3)
          location: rows=[6], cols=[3, 4, 5]
          size: [1, 3]
      dominant_orientation: horizontal
    output:
      grid_size: [10, 10]
      base_grid: same as input
      added_feature:
        shape: vertical line
        color: azure (8)
        location: rows=[0-9], cols=[9] (rightmost column)
        size: [10, 1]
      relationship: Added vertical line on the right border because input shapes were horizontal. Color is azure (8).

  train_2:
    input:
      grid_size: [10, 10]
      background_color: white (0)
      objects: # Can be viewed as a block or individual columns
        - shape: vertical line
          color: orange (7)
          location: rows=[3, 4, 5, 6], cols=[2]
          size: [4, 1]
        - shape: vertical line
          color: azure (8)
          location: rows=[3, 4, 5, 6], cols=[3]
          size: [4, 1]
        - shape: vertical line
          color: maroon (9)
          location: rows=[3, 4, 5, 6], cols=[4]
          size: [4, 1]
        - shape: vertical line
          color: blue (1)
          location: rows=[3, 4, 5, 6], cols=[5]
          size: [4, 1]
      dominant_orientation: vertical # Based on constituent lines
    output:
      grid_size: [10, 10]
      base_grid: same as input
      added_feature:
        shape: horizontal line
        color: azure (8)
        location: rows=[0], cols=[0-9] (topmost row)
        size: [1, 10]
      relationship: Added horizontal line on the top border because input shapes were vertical. Color is azure (8).

derived_rules:
  - rule: Determine the dominant orientation of non-background objects/shapes in the input grid.
    details: Check if connected non-background pixels form shapes that are wider than tall (horizontal) or taller than wide (vertical).
  - rule: If the dominant orientation is horizontal, add a vertical line of azure (8) color to the rightmost column of the grid.
  - rule: If the dominant orientation is vertical, add a horizontal line of azure (8) color to the topmost row of the grid.
  - rule: If orientation is ambiguous (e.g., square shapes), assume a default or apply tie-breaking (example suggests vertical takes precedence if components are vertical). The examples provided have clear or component-based orientation.
  - rule: The added color is always azure (8).
```


## Natural Language Program

1.  Analyze the input grid to identify all connected shapes formed by non-white pixels.
2.  Determine the primary orientation of these shapes:
    *   Calculate the width and height of the bounding box for each distinct non-white shape.
    *   If the shapes are predominantly wider than tall (sum of widths > sum of heights, or average width > average height), classify the dominant orientation as "horizontal".
    *   If the shapes are predominantly taller than wide, classify the dominant orientation as "vertical". (Consider constituent parts if a shape is complex, like the block in train_2 being composed of vertical lines). If shapes are square (width == height), potentially default to "vertical" based on `train_2`.
3.  Create the output grid by copying the input grid.
4.  Based on the determined dominant orientation:
    *   If "horizontal", fill the entire rightmost column of the output grid with azure (8).
    *   If "vertical", fill the entire topmost row of the output grid with azure (8).
5.  Return the modified grid.
```python
"""
Determines the dominant orientation of non-background shapes in the input grid.
If all shapes are strictly horizontal (width > height), adds a vertical line of azure (8) to the rightmost column.
Otherwise (if any shape is vertical (height > width), square (height == width), or if there's a mix of orientations), adds a horizontal line of azure (8) to the topmost row.
"""

import numpy as np
from typing import List, Tuple, Set

def find_objects(grid: np.ndarray, background_color: int = 0) -> List[Set[Tuple[int, int]]]:
    """
    Finds connected components of non-background pixels in the grid.

    Args:
        grid: The input grid as a numpy array.
        background_color: The integer value representing the background color (default 0).

    Returns:
        A list of sets, where each set contains the (row, col) coordinates of a connected object.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is not background and not visited yet
            if grid[r, c] != background_color and (r, c) not in visited:
                obj_coords = set()
                q = [(r, c)]  # Queue for BFS
                visited.add((r, c))
                
                # Breadth-First Search to find all connected pixels of the object
                while q:
                    curr_r, curr_c = q.pop(0)
                    obj_coords.add((curr_r, curr_c))
                    
                    # Check 4 adjacent neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check bounds and if neighbor is part of the object and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != background_color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def get_bounding_box(coords: Set[Tuple[int, int]]) -> Tuple[int, int]:
    """
    Calculates the height and width of the bounding box for a set of coordinates.

    Args:
        coords: A set of (row, col) tuples representing an object.

    Returns:
        A tuple containing the height and width of the bounding box.
        Returns (0, 0) if coords is empty.
    """
    if not coords:
        return 0, 0
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height, width

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on the dominant orientation of its non-background objects.

    Args:
        input_grid: A List of Lists representing the input grid.

    Returns:
        A List of Lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    rows, cols = output_grid.shape
    azure_color = 8

    # Find all non-background objects
    objects = find_objects(input_np)

    # Handle case with no objects (return copy)
    if not objects:
        return output_grid.tolist()

    # Determine dominant orientation
    is_strictly_horizontal_dominant = True
    
    for obj_coords in objects:
        h, w = get_bounding_box(obj_coords)
        # If any object is not strictly wider than tall, the dominance is not strictly horizontal
        if w <= h:
            is_strictly_horizontal_dominant = False
            break # No need to check further

    # Modify the output grid based on the determined orientation
    if is_strictly_horizontal_dominant:
        # If all objects are wider than tall, add vertical azure line to the rightmost column
        if cols > 0: # Ensure there is a column to modify
             output_grid[:, -1] = azure_color
    else:
        # Otherwise (vertical, square, or mixed objects), add horizontal azure line to the topmost row
         if rows > 0: # Ensure there is a row to modify
            output_grid[0, :] = azure_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```

Previous Code:
```python
"""
Determines the dominant orientation of non-background shapes in the input grid.
If all shapes are strictly horizontal (width > height), adds a vertical line of azure (8) to the rightmost column.
Otherwise (if any shape is vertical (height > width), square (height == width), or if there's a mix of orientations), adds a horizontal line of azure (8) to the topmost row.
"""

import numpy as np
from typing import List, Tuple, Set

def find_objects(grid: np.ndarray, background_color: int = 0) -> List[Set[Tuple[int, int]]]:
    """
    Finds connected components of non-background pixels in the grid.

    Args:
        grid: The input grid as a numpy array.
        background_color: The integer value representing the background color (default 0).

    Returns:
        A list of sets, where each set contains the (row, col) coordinates of a connected object.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is not background and not visited yet
            if grid[r, c] != background_color and (r, c) not in visited:
                obj_coords = set()
                q = [(r, c)]  # Queue for BFS
                visited.add((r, c))
                
                # Breadth-First Search to find all connected pixels of the object
                while q:
                    curr_r, curr_c = q.pop(0)
                    obj_coords.add((curr_r, curr_c))
                    
                    # Check 4 adjacent neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check bounds and if neighbor is part of the object and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != background_color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def get_bounding_box(coords: Set[Tuple[int, int]]) -> Tuple[int, int]:
    """
    Calculates the height and width of the bounding box for a set of coordinates.

    Args:
        coords: A set of (row, col) tuples representing an object.

    Returns:
        A tuple containing the height and width of the bounding box.
        Returns (0, 0) if coords is empty.
    """
    if not coords:
        return 0, 0
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height, width

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on the dominant orientation of its non-background objects.

    Args:
        input_grid: A List of Lists representing the input grid.

    Returns:
        A List of Lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    rows, cols = output_grid.shape
    azure_color = 8

    # Find all non-background objects
    objects = find_objects(input_np)

    # Handle case with no objects (return copy)
    if not objects:
        return output_grid.tolist()

    # Determine dominant orientation
    is_strictly_horizontal_dominant = True
    
    for obj_coords in objects:
        h, w = get_bounding_box(obj_coords)
        # If any object is not strictly wider than tall, the dominance is not strictly horizontal
        if w <= h:
            is_strictly_horizontal_dominant = False
            break # No need to check further

    # Modify the output grid based on the determined orientation
    if is_strictly_horizontal_dominant:
        # If all objects are wider than tall, add vertical azure line to the rightmost column
        if cols > 0: # Ensure there is a column to modify
             output_grid[:, -1] = azure_color
    else:
        # Otherwise (vertical, square, or mixed objects), add horizontal azure line to the topmost row
         if rows > 0: # Ensure there is a row to modify
            output_grid[0, :] = azure_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 4 4 4 0 0 0 8
0 0 0 2 2 2 0 0 0 8
0 0 0 3 3 3 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 18
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 18.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

*code_execution:*
```python
## Assessment

The previous code version successfully transformed `train_2` but failed on `train_1`. The code generated the top horizontal azure line for `train_1`, whereas the expected output has a right vertical azure line.

The core logic involved identifying non-background objects and checking their dimensions (height `h`, width `w`). The transformation rule was intended to be: if all objects are strictly wider than tall (`w > h`), add a right vertical line; otherwise, add a top horizontal line.

Analysis of `train_1` shows three distinct horizontal line objects (yellow, red, green), each with dimensions h=1, w=3. Since `w > h` for all objects, the condition "all objects are strictly wider than tall" should have been met, triggering the addition of the right vertical line. The fact that the top horizontal line was added instead suggests either a flaw in the implementation of the conditional logic or an issue with how objects/dimensions were identified in the failed execution.

Analysis of `train_2` shows four distinct vertical line objects (orange, azure, maroon, blue), each with h=4, w=1. Since `w <= h` for these objects, the condition "all objects are strictly wider than tall" is *not* met. Therefore, the code correctly fell into the "otherwise" case and added the top horizontal line.

The revised strategy will refine the logic based on the *presence* of specific orientations rather than a universal condition ("all objects must be...").

**Strategy:**
1.  Identify distinct objects based on contiguous pixels of the *same* non-background color (aligning with ARC priors).
2.  For each object, determine its bounding box height (`h`) and width (`w`).
3.  Check if *any* object exists where `w > h` (a horizontal object is present).
4.  Check if *any* object exists where `h > w` (a vertical object is present).
5.  Apply the transformation:
    *   If horizontal objects are present AND vertical objects are *not* present, add a vertical azure line to the rightmost column.
    *   In all other cases (only vertical objects present, both vertical and horizontal objects present, only square objects present, or mixtures including squares), add a horizontal azure line to the topmost row.
6.  Update the documentation (facts, natural language program) to reflect this refined logic.

## Metrics

Metrics gathered using the helper functions `find_objects_same_color` (finds contiguous objects of the same color) and `get_bounding_box`.
<ctrl97>tool_code
import numpy as np
from typing import List, Tuple, Set

# Helper functions
def find_objects_same_color(grid: np.ndarray, background_color: int = 0) -> List[Set[Tuple[int, int]]]:
    rows, cols = grid.shape
    visited = set()
    objects = []
    for r in range(rows):
        for c in range(cols):
            pixel_color = grid[r, c]
            if pixel_color != background_color and (r, c) not in visited:
                obj_coords = set()
                q = [(r, c)]
                visited.add((r, c))
                while q:
                    curr_r, curr_c = q.pop(0)
                    obj_coords.add((curr_r, curr_c))
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check bounds AND same color AND not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == pixel_color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def get_bounding_box(coords: Set[Tuple[int, int]]) -> Tuple[int, int]:
    if not coords: return 0, 0
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height, width

# Example inputs
train_1_input = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 4, 4, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 3, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

train_2_input = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 7, 8, 9, 1, 0, 0, 0, 0],
    [0, 0, 7, 8, 9, 1, 0, 0, 0, 0], [0, 0, 7, 8, 9, 1, 0, 0, 0, 0],
    [0, 0, 7, 8, 9, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

# Analyze train_1
objects_1 = find_objects_same_color(train_1_input)
dims_1 = [get_bounding_box(obj) for obj in objects_1]
has_vertical_1 = any(h > w for h, w in dims_1)
has_horizontal_1 = any(w > h for h, w in dims_1)

# Analyze train_2
objects_2 = find_objects_same_color(train_2_input)
dims_2 = [get_bounding_box(obj) for obj in objects_2]
has_vertical_2 = any(h > w for h, w in dims_2)
has_horizontal_2 = any(w > h for h, w in dims_2)

print(f"Train 1 Objects: {len(objects_1)}, Dimensions (H, W): {dims_1}")
print(f"Train 1 Presence: Vertical? {has_vertical_1}, Horizontal? {has_horizontal_1}")
print(f"Train 2 Objects: {len(objects_2)}, Dimensions (H, W): {dims_2}")
print(f"Train 2 Presence: Vertical? {has_vertical_2}, Horizontal? {has_horizontal_2}")
```

*code_execution_result:*
outcome: OUTCOME_FAILED
```
Traceback (most recent call last):
  File "<string>", line 142
    It seems the logic derived ("Add right line only if only horizontal objects exist, otherwise add top line") works regardless of whether we define objects by same-color or any-non-background color connectivity, *as long as* we use the same definition consistently. The ARC prior definition ("contiguous block of one or more pixels of the same color") suggests using `find_objects_same_color`. The previous code used the any-non-background version (`find_objects`). Let's stick with the ARC prior and use same-color objects.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       ^
SyntaxError: unterminated string literal (detected at line 142)

```
## Facts


```yaml
task_description: Modify the input grid by adding a single line of azure (8) color along one edge. The edge and orientation of the line depend on the orientation of the shapes present in the input grid.

definitions:
  background_color: white (0)
  object: A contiguous block of one or more pixels of the same non-background color. Adjacent pixels are defined by sharing an edge (4-connectivity).
  object_bounding_box: The smallest rectangle enclosing all pixels of an object.
  object_height (h): The height of the object's bounding box.
  object_width (w): The width of the object's bounding box.
  horizontal_object: An object where width > height.
  vertical_object: An object where height > width.
  square_object: An object where height == width.
  added_line_color: azure (8)

examples:
  train_1:
    input:
      grid_size: [10, 10]
      background_color: white (0)
      objects:
        - color: yellow (4), location: rows=[4], cols=[3, 4, 5], bounding_box: [h=1, w=3], orientation: horizontal
        - color: red (2), location: rows=[5], cols=[3, 4, 5], bounding_box: [h=1, w=3], orientation: horizontal
        - color: green (3), location: rows=[6], cols=[3, 4, 5], bounding_box: [h=1, w=3], orientation: horizontal
      presence: Contains horizontal objects? Yes. Contains vertical objects? No.
    output:
      base_grid: same as input
      added_feature: Vertical line, color=azure (8), location=rightmost column (cols=[9]).
      reasoning: Only horizontal objects were present.

  train_2:
    input:
      grid_size: [10, 10]
      background_color: white (0)
      objects:
        - color: orange (7), location: rows=[3-6], cols=[2], bounding_box: [h=4, w=1], orientation: vertical
        - color: azure (8), location: rows=[3-6], cols=[3], bounding_box: [h=4, w=1], orientation: vertical
        - color: maroon (9), location: rows=[3-6], cols=[4], bounding_box: [h=4, w=1], orientation: vertical
        - color: blue (1), location: rows=[3-6], cols=[5], bounding_box: [h=4, w=1], orientation: vertical
      presence: Contains horizontal objects? No. Contains vertical objects? Yes.
    output:
      base_grid: same as input
      added_feature: Horizontal line, color=azure (8), location=topmost row (rows=[0]).
      reasoning: Only vertical objects were present (falls under the 'otherwise' condition).

derived_rules:
  - rule: Identify all distinct objects (contiguous same-colored non-background pixels) in the input grid.
  - rule: Determine the bounding box dimensions (height `h`, width `w`) for each object.
  - rule: Check if at least one object has `w > h` (presence of horizontal objects).
  - rule: Check if at least one object has `h > w` (presence of vertical objects).
  - rule: If horizontal objects are present AND vertical objects are NOT present, then add a vertical line of azure (8) to the rightmost column of the grid.
  - rule: Otherwise (if only vertical objects are present, if both horizontal and vertical objects are present, if only square objects are present, or if no objects are present), add a horizontal line of azure (8) to the topmost row of the grid.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Find all distinct objects in the input grid. An object is defined as a contiguous area of pixels having the same non-background color (using 4-way adjacency).
3.  If no objects are found, add a horizontal line of azure (8) to the topmost row of the output grid and return it.
4.  For each found object, calculate the height (`h`) and width (`w`) of its bounding box.
5.  Determine if there exists at least one object for which `w > h` (set flag `has_horizontal`).
6.  Determine if there exists at least one object for which `h > w` (set flag `has_vertical`).
7.  Apply the transformation based on the flags:
    *   If `has_horizontal` is true AND `has_vertical` is false: Modify the output grid by setting all pixels in the rightmost column to azure (8).
    *   Otherwise (if `has_vertical` is true, or if both flags are true, or if neither flag is true): Modify the output grid by setting all pixels in the topmost row to azure (8).
8.  Return the modified output grid.
