
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 4 8 8 8 8 8 8 8
8 8 7 1 6 5 6 1 8 8
8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 2 8 8 8 8 8 8 8
8 8 1 6 5 6 1 7 8 8
8 8 8 8 8 8 8 4 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8
8 8 1 8 8 8 8 8 8 8
8 8 7 8 8 8 8 8 8 8
8 8 9 6 8 8 8 8 8 8
8 8 8 4 7 7 8 8 8 8
8 8 8 8 8 1 8 8 8 8
8 8 8 8 8 4 8 8 8 8
8 8 8 8 8 4 2 1 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8
8 8 1 8 8 8 8 8 8 8
8 8 2 8 8 8 8 8 8 8
8 8 4 4 8 8 8 8 8 8
8 8 8 1 7 7 8 8 8 8
8 8 8 8 8 4 8 8 8 8
8 8 8 8 8 6 8 8 8 8
8 8 8 8 8 9 7 1 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
```

*   **Perception of Elements:**
    *   The input and output grids are the same size (10x10).
    *   Both grids have a dominant background color: azure (8).
    *   In both examples, there is a single connected object composed of non-azure pixels.
    *   The shape and position of this object remain the same from input to output.
    *   The colors of the pixels *within* the object change.
    *   The object in `train_1` is an 'L' shape with a horizontal segment and two vertical pixels attached at the ends. The object in `train_2` is a more complex, snake-like path.
    *   Comparing the input and output colors for the object suggests a transformation based on the object's structure. Specifically, the object appears to behave like a path or sequence.

*   **YAML Facts:**
    
```yaml
    task_context:
      grid_size: constant (10x10 in examples)
      background_color: azure (8)
      num_objects: 1 (connected component of non-background pixels)

    object_properties:
      type: connected component of non-background pixels
      structure: path-like (a sequence of connected pixels)
      invariance: position and shape remain constant between input and output
      endpoints: two pixels within the object having only one object neighbor (degree 1 nodes in the object graph)

    transformation:
      action: modify colors within the object
      rule: reverse the sequence of colors along the path connecting the two endpoints
      details:
        - identify the object pixels
        - find the two endpoint pixels
        - trace the path between endpoints
        - extract the color sequence along the path
        - reverse the color sequence
        - map the reversed colors back onto the path pixels in the output grid

    relationships:
      - pixels within the object are connected adjacently (including diagonals)
      - endpoints define the start and end of the color sequence to be reversed
      - background pixels are unchanged
    ```


*   **Natural Language Program:**
    1.  Identify the single connected object formed by pixels that are not the background color (azure, 8).
    2.  Find the two endpoint pixels of this object. An endpoint is an object pixel connected to only one other object pixel (considering 8-way adjacency).
    3.  Determine the unique path (sequence of adjacent pixels) that connects these two endpoints within the object.
    4.  Extract the list of colors corresponding to the pixels along this path, starting from one endpoint and proceeding to the other.
    5.  Reverse the order of the colors in this list.
    6.  Create the output grid by copying the input grid.
    7.  Replace the color of each pixel along the path in the output grid with the color at the corresponding position in the reversed list. Keep all background pixels unchanged.
```python
import numpy as np
from collections import deque

"""
Identifies a single connected object of non-background pixels (azure, 8). 
Finds the two endpoints of this object (pixels with only one object neighbor).
Traces the path connecting these endpoints.
Extracts the colors along this path, reverses the color sequence, and applies 
the reversed sequence back onto the path pixels in the output grid. 
The background remains unchanged.
"""

def get_neighbors(coord, grid_shape, connectivity=8):
    """Gets valid neighbor coordinates for a given coordinate."""
    r, c = coord
    rows, cols = grid_shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            if connectivity == 4 and abs(dr) + abs(dc) != 1:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def find_object_pixels(grid, background_color):
    """Finds all coordinates belonging to non-background objects."""
    object_pixels = set()
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color:
                object_pixels.add((r, c))
    return object_pixels

def find_endpoints(object_pixels, grid_shape):
    """Finds endpoint pixels within the object set."""
    endpoints = []
    for r, c in object_pixels:
        neighbor_count = 0
        for nr, nc in get_neighbors((r, c), grid_shape, connectivity=8):
            if (nr, nc) in object_pixels:
                neighbor_count += 1
        if neighbor_count == 1:
            endpoints.append((r, c))
    return endpoints

def find_path_bfs(start, end, object_pixels, grid_shape):
    """Finds the path between start and end points using BFS within object pixels."""
    if start not in object_pixels or end not in object_pixels:
        return None

    queue = deque([(start, [start])]) # Store (current_coord, path_so_far)
    visited = {start}

    while queue:
        current_coord, path = queue.popleft()

        if current_coord == end:
            return path

        for neighbor in get_neighbors(current_coord, grid_shape, connectivity=8):
            if neighbor in object_pixels and neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append((neighbor, new_path))

    return None # Path not found

def transform(input_grid):
    """
    Reverses the color sequence along the path connecting the endpoints 
    of the single non-background object.
    """
    # Convert input to numpy array for easier handling
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    grid_shape = input_grid_np.shape
    
    # Define background color (assuming 8 based on examples)
    background_color = 8 

    # 1. Identify the object pixels
    object_pixels = find_object_pixels(input_grid_np, background_color)

    if not object_pixels:
        # No object found, return the original grid
        return output_grid.tolist() 

    # 2. Find the endpoints
    endpoints = find_endpoints(object_pixels, grid_shape)

    # Expect exactly two endpoints for a simple path
    if len(endpoints) != 2:
        # Unexpected structure, return original grid 
        # (or handle differently based on more examples/rules)
         return output_grid.tolist()

    start_node, end_node = endpoints[0], endpoints[1]

    # 3. Determine the path between endpoints
    path_coords = find_path_bfs(start_node, end_node, object_pixels, grid_shape)

    if path_coords is None:
         # Path not found (shouldn't happen if endpoints are correct for a single connected object)
         return output_grid.tolist() 

    # 4. Extract the list of colors along the path
    path_colors = [input_grid_np[r, c] for r, c in path_coords]

    # 5. Reverse the order of the colors
    reversed_colors = path_colors[::-1]

    # 6. Create the output grid (already copied)
    # 7. Replace colors along the path with reversed colors
    for i, (r, c) in enumerate(path_coords):
        output_grid[r, c] = reversed_colors[i]

    # Return the modified grid as a list of lists
    return output_grid.tolist()
```
