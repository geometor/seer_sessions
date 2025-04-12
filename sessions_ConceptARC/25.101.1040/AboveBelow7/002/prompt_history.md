
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 4 4 4 4 4 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 4 4 4 4 4 4 4 4 0 0 0
```


## train_2

**input:**
```
0 0 0 8 8 0 0 0 0 0 0 0
0 0 8 8 8 8 0 0 0 8 0 0
0 8 8 8 8 8 8 0 8 8 8 0
0 2 2 2 2 2 2 0 2 2 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 2 2 0
0 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 0 2 2 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 2 2 0
0 2 2 2 2 2 2 0 0 8 0 0
0 0 0 8 8 0 0 0 8 8 8 0
0 0 8 8 8 8 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task based on the provided examples.

**Perception of the Elements:**

1.  **Input/Output Structure:** Both input and output are grids of pixels with different colors. The background is consistently white (0).
2.  **Objects:** In each example pair, the input grid contains exactly two distinct, contiguous, non-white colored objects.
    *   `train_1`: A solid yellow (4) rectangle and a hollow green (3) rectangle (frame).
    *   `train_2`: An irregular azure (8) shape and a hollow red (2) rectangle (frame).
3.  **Spatial Relationship (Input):** In both examples, one object is located entirely above the other object. There is no horizontal overlap, and in these specific examples, there is no vertical gap between their bounding boxes.
    *   `train_1`: Yellow object is above the Green object.
    *   `train_2`: Azure object is above the Red object.
4.  **Transformation:** The core transformation appears to be a vertical swap of the two objects. The object that was originally lower remains in its original vertical position, while the object that was originally upper is moved below it.
5.  **Properties Preservation:** The shape, color, and internal structure of each object remain unchanged during the transformation. The relative horizontal positions also seem preserved. The vertical gap (if any) between the objects is also preserved after the swap.

**YAML Facts:**


```yaml
task_context:
  description: Swaps the vertical positions of two distinct non-background objects where one is directly above the other.
  grid_properties:
    background_color: 0 # white
    max_colors: 3 # background + 2 objects

input_elements:
  - element_type: object
    count: 2
    properties:
      - color: non-zero
      - contiguity: contiguous pixels of the same color
      - relative_position: One object is strictly above the other (no row overlap).
      - name: upper_object
      - name: lower_object

output_elements:
  - element_type: object
    count: 2
    properties:
      - color: same as corresponding input objects
      - shape: same as corresponding input objects
      - contiguity: same as corresponding input objects
      - relative_position: The original lower_object is now above the original upper_object.
      - name: new_upper_object (originally lower_object)
      - name: new_lower_object (originally upper_object)

transformation:
  action: vertical_swap
  details:
    - Identify the two distinct non-white objects.
    - Determine which object is 'upper' and which is 'lower' based on row indices.
    - Calculate the vertical gap between the bottom row of the upper object and the top row of the lower object.
    - In the output grid:
        - Place the original 'lower' object at its original coordinates.
        - Place the original 'upper' object below the (now positioned) original 'lower' object, preserving the original vertical gap between them.
  preserves:
    - Object shape and color.
    - Object internal structure.
    - Relative horizontal positioning.
    - Vertical gap between objects.
```


**Natural Language Program:**

1.  Identify all distinct contiguous groups of non-white pixels in the input grid. These are the 'objects'. Assume there are exactly two such objects.
2.  For each object, determine its bounding box (minimum and maximum row and column indices).
3.  Identify the 'upper object' as the one with the smaller minimum row index, and the 'lower object' as the one with the larger minimum row index.
4.  Calculate the vertical gap between the objects: `gap = lower_object.min_row - upper_object.max_row - 1`.
5.  Create a new output grid of the same dimensions as the input, filled with the background color (white).
6.  Copy the pixels belonging to the 'lower object' from the input grid to the output grid, maintaining their original row and column coordinates.
7.  Determine the new starting row for the 'upper object' in the output grid: `new_upper_object_start_row = lower_object.max_row + gap + 1`.
8.  Calculate the vertical shift needed for the upper object: `shift = new_upper_object_start_row - upper_object.min_row`.
9.  Copy the pixels belonging to the 'upper object' from the input grid to the output grid, adding the calculated `shift` to their original row coordinates while keeping their column coordinates the same.
```python
import numpy as np
from collections import deque

"""
Identifies the two distinct non-background objects in the input grid.
Determines which object is vertically above the other.
Calculates the vertical gap between them.
Creates an output grid where the original lower object maintains its position,
and the original upper object is moved below the lower object, preserving the original vertical gap.
"""

def find_objects(grid: np.ndarray) -> list[dict]:
    """
    Finds distinct contiguous objects of non-background colors.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, each representing an object with its 
        color, coordinates, and bounding box.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # If it's a non-background color and not visited yet
            if color != 0 and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
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
                    'coords': obj_coords,
                    'bbox': (min_r, max_r, min_c, max_c) # min_row, max_row, min_col, max_col
                })
    return objects

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Swaps the vertical positions of two distinct non-background objects 
    where one is directly above the other. The lower object stays in place, 
    and the upper object moves below it, maintaining the original vertical gap.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # Initialize output grid with background color (0)
    output_array = np.zeros_like(input_array)

    # Find the objects
    objects = find_objects(input_array)

    # Ensure exactly two objects were found
    if len(objects) != 2:
        # Handle error case or unexpected input - returning input for now
        print(f"Warning: Expected 2 objects, found {len(objects)}. Returning input.")
        return input_grid

    # Identify upper and lower objects based on min_row
    obj1 = objects[0]
    obj2 = objects[1]
    
    if obj1['bbox'][0] < obj2['bbox'][0]:
        upper_object = obj1
        lower_object = obj2
    else:
        upper_object = obj2
        lower_object = obj1

    # Extract bounding box info
    upper_min_r, upper_max_r, _, _ = upper_object['bbox']
    lower_min_r, lower_max_r, _, _ = lower_object['bbox']
    
    # Calculate the vertical gap between the objects
    # gap = bottom row of upper obj - top row of lower obj - 1
    gap = lower_min_r - upper_max_r - 1
    
    # Place the lower object in the output grid at its original position
    for r, c in lower_object['coords']:
        output_array[r, c] = lower_object['color']
        
    # Determine the new starting row for the upper object
    # It should start below the lower object, maintaining the gap
    # new_upper_top_row = bottom row of lower obj + gap + 1
    new_upper_object_start_row = lower_max_r + gap + 1
    
    # Calculate the vertical shift needed for the upper object
    shift = new_upper_object_start_row - upper_min_r
    
    # Place the upper object in the output grid at its new shifted position
    for r, c in upper_object['coords']:
        new_r = r + shift
        # Check bounds just in case, though logic should prevent out-of-bounds
        if 0 <= new_r < rows:
             output_array[new_r, c] = upper_object['color']
        else:
            print(f"Warning: Calculated new row {new_r} for upper object pixel at ({r},{c}) is out of bounds ({rows}x{cols}).")


    return output_array.tolist()
```
