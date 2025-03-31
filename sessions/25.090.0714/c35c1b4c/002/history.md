
## train_1

**input:**
```
9 0 0 0 0 7 7 0 9 0
0 0 9 0 0 0 9 9 9 0
7 7 0 3 3 3 3 7 9 7
0 3 7 3 3 3 3 9 3 7
0 3 9 3 3 0 0 0 3 9
9 3 3 3 3 0 0 9 3 0
3 3 3 3 3 9 0 0 3 7
3 3 3 3 3 0 9 9 3 0
0 9 0 3 3 3 9 9 9 9
7 9 7 9 0 0 7 7 0 0
```


**output:**
```
9 0 0 0 0 7 7 0 9 0
0 0 9 0 0 0 9 9 9 0
7 7 0 3 3 3 3 7 9 7
0 3 7 3 3 3 3 9 3 7
0 3 9 3 3 3 3 0 3 9
9 3 3 3 3 3 3 3 3 0
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
0 9 0 3 3 3 3 9 9 9
7 9 7 9 0 0 7 7 0 0
```


## train_2

**input:**
```
6 6 8 8 8 0 8 0 6 0
0 8 0 0 6 6 6 6 8 0
6 6 0 1 1 1 1 0 6 6
0 0 1 1 1 1 1 1 0 0
8 1 1 1 1 1 1 1 0 0
6 1 1 1 1 1 1 1 6 0
6 1 1 1 1 1 1 1 6 8
0 8 1 1 1 8 6 8 0 0
6 8 6 0 6 0 8 0 6 8
8 6 0 6 0 6 6 8 0 8
```


**output:**
```
6 6 8 8 8 0 8 0 6 0
0 8 0 0 6 6 6 6 8 0
6 6 0 1 1 1 1 0 6 6
0 0 1 1 1 1 1 1 0 0
8 1 1 1 1 1 1 1 1 0
6 1 1 1 1 1 1 1 1 0
6 1 1 1 1 1 1 1 1 8
0 8 1 1 1 1 1 1 0 0
6 8 6 0 6 0 8 0 6 8
8 6 0 6 0 6 6 8 0 8
```


## train_3

**input:**
```
1 1 0 1 1 0 0 0 4 1
4 4 0 4 2 2 1 4 4 4
4 0 2 2 2 2 2 2 1 0
0 4 2 2 2 0 0 1 1 0
0 0 1 2 2 2 1 0 1 0
0 4 0 2 2 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2
4 1 4 1 2 2 4 4 1 4
0 4 4 4 2 1 1 4 4 1
4 0 4 4 0 4 1 1 4 0
```


**output:**
```
1 1 0 1 1 0 0 0 4 1
4 4 0 4 2 2 1 4 4 4
4 0 2 2 2 2 2 2 1 0
0 4 2 2 2 2 2 2 1 0
0 0 1 2 2 2 2 0 1 0
0 4 0 2 2 2 2 0 0 0
2 2 2 2 2 2 2 2 2 2
4 1 4 1 2 2 4 4 1 4
0 4 4 4 2 2 1 4 4 1
4 0 4 4 0 4 1 1 4 0
```

*   **Perception:** The task involves identifying the largest contiguous block of a single non-white color within the input grid. This block acts like a container or boundary. Any pixel, regardless of its original color (including white/background), that falls "inside" this boundary is changed to the color of the boundary block itself. Pixels outside this boundary, and pixels that are part of the boundary block, remain unchanged. The concept of "inside" is determined by whether a pixel, if treated as empty space (along with all other pixels not part of the largest block), can reach the edge of the grid without crossing the largest block.

*   **Facts:**
    
```yaml
    major_object:
      description: The largest contiguous area of any single non-white color.
      properties:
        - color: The color C of the pixels forming this object.
        - size: The count of pixels in the object.
        - location: The set of coordinates {(r, c), ...} occupied by the object.
      selection_criterion: Maximum size among all contiguous non-white objects.
    enclosed_cells:
      description: Cells considered "inside" the major_object.
      identification:
        - Create a mask grid where major_object cells have color C and all others are white (0).
        - Identify all white cells in the mask grid that are not reachable from the grid boundary by traversing only white cells.
      location: The set of coordinates {(r, c), ...} of these enclosed cells.
    transformation:
      action: Fill enclosed cells.
      input: Original grid.
      output: Modified grid.
      rule: For each cell (r, c) corresponding to an enclosed_cell location, set its color to C in the output grid. All other cells retain their original color from the input grid.
    background_color: white (0) - Does not form objects of interest but can be part of the enclosed region.
    other_objects: Smaller contiguous non-white areas or individual pixels not part of the major object. They are treated as background when determining enclosure, and their color might be overwritten if they fall within the enclosed region.
    ```


*   **Natural Language Program:**
    1.  Find all contiguous areas of non-white pixels in the input grid.
    2.  Determine the area with the largest number of pixels (the "largest object"). Record its color, `C`.
    3.  Create a temporary grid (mask) of the same size as the input. Mark the locations of the largest object's pixels with `True` and all other locations with `False`.
    4.  Identify all `False` locations on the boundary of the mask grid.
    5.  Starting from these boundary `False` locations, perform a flood fill or breadth-first search to find all reachable `False` locations by moving only through adjacent `False` locations (horizontally and vertically). Mark these as "externally reachable".
    6.  Initialize the output grid as a copy of the input grid.
    7.  Iterate through every cell `(r, c)` in the grid. If the corresponding location `(r, c)` in the mask is `False` AND it was *not* marked as "externally reachable" in step 5, change the color of the cell `(r, c)` in the output grid to `C`.
    8.  The final state of the output grid is the result.
```python
import numpy as np
from collections import deque

def find_contiguous_objects(grid, ignore_color=0):
    """
    Finds all contiguous objects of the same color in a grid, ignoring a specified color.

    Args:
        grid (np.array): The input grid.
        ignore_color (int): The color value to ignore (usually background).

    Returns:
        list: A list of tuples, where each tuple represents an object and contains
              (color, set_of_coordinates). Returns an empty list if no objects are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != ignore_color and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    
                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if obj_coords:
                    objects.append((color, obj_coords))
                    
    return objects

def find_largest_object(objects):
    """
    Finds the object with the most pixels from a list of objects.

    Args:
        objects (list): A list of objects, where each object is (color, set_of_coordinates).

    Returns:
        tuple: The largest object (color, set_of_coordinates), or None if the list is empty.
    """
    if not objects:
        return None
    
    largest_obj = max(objects, key=lambda obj: len(obj[1]))
    return largest_obj

def find_externally_reachable(grid_shape, boundary_coords):
    """
    Finds all cells not part of the boundary that can be reached from the grid edges.

    Args:
        grid_shape (tuple): The (rows, cols) dimensions of the grid.
        boundary_coords (set): A set of (row, col) coordinates representing the boundary object.

    Returns:
        set: A set of (row, col) coordinates representing cells reachable from the outside.
    """
    rows, cols = grid_shape
    reachable = set()
    q = deque()
    
    # Add all non-boundary cells on the edges to the queue
    for r in range(rows):
        if (r, 0) not in boundary_coords:
            if (r, 0) not in reachable:
                q.append((r, 0))
                reachable.add((r, 0))
        if (r, cols - 1) not in boundary_coords:
             if (r, cols - 1) not in reachable:
                q.append((r, cols - 1))
                reachable.add((r, cols - 1))
                
    for c in range(cols):
        if (0, c) not in boundary_coords:
             if (0, c) not in reachable:
                q.append((0, c))
                reachable.add((0, c))
        if (rows - 1, c) not in boundary_coords:
            if (rows - 1, c) not in reachable:
                q.append((rows - 1, c))
                reachable.add((rows - 1, c))

    # Perform BFS to find all reachable cells
    while q:
        r, c = q.popleft()
        
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < rows and 0 <= nc < cols and \
               (nr, nc) not in boundary_coords and (nr, nc) not in reachable:
                reachable.add((nr, nc))
                q.append((nr, nc))
                
    return reachable


def transform(input_grid):
    """
    Transforms the input grid by finding the largest contiguous non-white object,
    identifying all cells enclosed by it, and filling those enclosed cells with
    the color of the largest object.

    1. Find all contiguous areas of non-white pixels.
    2. Determine the area with the largest number of pixels (the "largest object").
    3. Identify all cells not part of the largest object that cannot reach the
       grid boundary without crossing the largest object (the "enclosed cells").
    4. Create the output grid by copying the input grid.
    5. Change the color of the enclosed cells in the output grid to the color
       of the largest object.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    
    # 1. Find all contiguous non-white objects
    objects = find_contiguous_objects(input_grid_np, ignore_color=0)
    
    # If no non-white objects exist, return the original grid
    if not objects:
        return input_grid_np.tolist()
        
    # 2. Find the largest object
    largest_object = find_largest_object(objects)
    if largest_object is None: # Should not happen if objects list is not empty, but safe check
         return input_grid_np.tolist()

    largest_object_color, largest_object_coords = largest_object
    
    # 3. Identify externally reachable non-boundary cells
    externally_reachable_coords = find_externally_reachable(input_grid_np.shape, largest_object_coords)

    # 4. Initialize output grid
    output_grid = np.copy(input_grid_np)
    
    # 5. Iterate through all cells and fill enclosed ones
    for r in range(rows):
        for c in range(cols):
            coord = (r, c)
            # If a cell is NOT part of the largest object AND NOT externally reachable,
            # it is considered enclosed.
            if coord not in largest_object_coords and coord not in externally_reachable_coords:
                output_grid[r, c] = largest_object_color
                
    return output_grid.tolist()
```
