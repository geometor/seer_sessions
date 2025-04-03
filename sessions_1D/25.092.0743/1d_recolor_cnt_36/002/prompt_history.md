
## train_1

**input:**
```
0 0 0 7 0 0 0 7 7 7 0 7 7 0 0 0 7 0 0 7 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 3 0 0 0 6 6 6 0 2 2 0 0 0 3 0 0 3 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 7 0 0 7 7 7 0 0 0 7 7 0 0 0 7 7 7 0 0 7 7 0 0 0 0 0 0
```


**output:**
```
0 0 3 0 0 6 6 6 0 0 0 2 2 0 0 0 6 6 6 0 0 2 2 0 0 0 0 0 0
```


## train_3

**input:**
```
0 7 7 0 7 7 7 0 7 0 0 0 7 7 0 7 7 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2 0 6 6 6 0 3 0 0 0 2 2 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, analyzing the task examples.

**Perception:**
The input grids contain white pixels (0) and orange pixels (7). The orange pixels form distinct, non-overlapping objects (contiguous groups). The output grids have the same dimensions as the input grids. The white pixels remain unchanged. The orange pixels in the input are replaced by different colors in the output: green (3), magenta (6), or red (2). The color used for replacement seems to depend on the properties of the original orange object.

Observing the examples:
- In `train_1`, single orange pixels become green, a 1x3 horizontal line becomes magenta, and a 2x2 square becomes red.
- In `train_2`, the same pattern holds: single orange becomes green, 1x3 lines become magenta, 2x2 squares become red.
- In `train_3`, the pattern confirms: 2x2 squares become red, a 1x3 line becomes magenta, and a single orange pixel becomes green.

It appears the transformation rule is based on the *size* (number of pixels) of each distinct orange object:
- Objects of size 1 become green (3).
- Objects of size 3 become magenta (6).
- Objects of size 4 become red (2).

**Facts:**

```yaml
task_context:
  - The input grid contains white (0) and orange (7) pixels.
  - The output grid retains the white (0) pixels in their original positions.
  - Orange (7) pixels in the input are replaced by other colors in the output.
objects:
  - type: contiguous_group
    color: orange (7)
    properties:
      - size: number of pixels in the group
transformations:
  - action: identify_objects
    input_color: orange (7)
    output: set of distinct orange objects
  - action: for_each_object
    condition: object size == 1
    result: change all pixels of the object to green (3)
  - action: for_each_object
    condition: object size == 3
    result: change all pixels of the object to magenta (6)
  - action: for_each_object
    condition: object size == 4
    result: change all pixels of the object to red (2)
grid_properties:
  - dimensions remain unchanged.
  - background (white pixels) remains unchanged.
relationships:
  - The output color of a transformed object depends solely on the size of the corresponding input object.
```


**Natural Language Program:**
1.  Initialize the output grid as a copy of the input grid.
2.  Find all distinct contiguous objects composed of orange (7) pixels in the input grid.
3.  For each identified orange object:
    a.  Calculate the size of the object (the number of pixels it contains).
    b.  Determine the target color based on the object's size:
        i.  If the size is 1, the target color is green (3).
        ii. If the size is 3, the target color is magenta (6).
        iii. If the size is 4, the target color is red (2).
    c.  In the output grid, replace all pixels corresponding to the locations of the current orange object with the determined target color.
4.  Return the modified output grid.
```python
import numpy as np
from collections import deque

"""
Identifies contiguous objects of orange (7) pixels in the input grid.
Determines the size (number of pixels) of each orange object.
Replaces the orange pixels of each object in the output grid with a new color based on the object's size:
- Size 1: Replace with green (3).
- Size 3: Replace with magenta (6).
- Size 4: Replace with red (2).
All other pixels (including white background) remain unchanged.
"""

def find_objects(grid, color):
    """
    Finds all connected components (objects) of a given color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is a list of (row, col) tuples.
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # If we find a pixel of the target color that hasn't been visited, start a search
            if grid[r, c] == color and not visited[r, c]:
                current_object_coords = []
                q = deque([(r, c)])  # Use deque for efficient BFS queue
                visited[r, c] = True

                while q:
                    row, col = q.popleft() # BFS
                    current_object_coords.append((row, col))

                    # Check neighbors (4-way adjacency: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check bounds and if the neighbor is the target color and not visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Add the found object (list of coordinates) to our list of objects
                if current_object_coords:
                    objects.append(current_object_coords)
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on the size of orange objects.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Define colors
    orange_color = 7
    green_color = 3
    magenta_color = 6
    red_color = 2

    # Find all distinct orange objects in the input grid
    orange_objects = find_objects(input_grid, orange_color)

    # Iterate through each found orange object
    for obj_coords in orange_objects:
        # Calculate the size of the current object
        obj_size = len(obj_coords)

        # Determine the target color based on the object's size
        target_color = -1 # Initialize with a value indicating no rule matched
        if obj_size == 1:
            target_color = green_color
        elif obj_size == 3:
            target_color = magenta_color
        elif obj_size == 4:
            target_color = red_color

        # If a size rule matched, change the pixels in the output grid
        if target_color != -1:
            for r, c in obj_coords:
                output_grid[r, c] = target_color
        # If no rule matched (e.g., size 2 or 5+), the pixels retain their original orange color
        # because output_grid was initialized as a copy of input_grid.

    return output_grid
```
